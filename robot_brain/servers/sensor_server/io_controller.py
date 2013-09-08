import numpy as np
from matplotlib.pyplot import Figure
from mpl_toolkits.mplot3d import Axes3D
from enable.api import Component
from traits.api import (HasStrictTraits, Int, Float, Instance, Any, Dict,
                        on_trait_change, Set, List, NO_COMPARE)
from chaco.api import Plot, ArrayPlotData

from links_component import LinksComponent


# Map of input names and the amount needed to normalize them
INPUT_MAP = [('potentiometer', 1024.0),
            ('distance', 100.0),
            ('switch', 1),
            ('acc_z', 1024.0),
            ('acc_y', 1024.0),
            ('acc_x', 1024.0)]

OUTPUT_MAP = ['motor', 'servo', 'led']


class IOController(HasStrictTraits):

    ### Current Sensor Values  ################################################

    acc_x = Float(plot_data=True, comparison_mode=NO_COMPARE)

    acc_y = Float(plot_data=True, comparison_mode=NO_COMPARE)

    acc_z = Float(plot_data=True, comparison_mode=NO_COMPARE)

    switch = Float(plot_data=True, comparison_mode=NO_COMPARE)

    distance = Float(plot_data=True, comparison_mode=NO_COMPARE)

    potentiometer = Float(plot_data=True, comparison_mode=NO_COMPARE)

    ### Plots  ################################################################

    logo_plot = Instance(Figure)

    acc_x_plot = Instance(Plot)

    acc_y_plot = Instance(Plot)

    acc_z_plot = Instance(Plot)

    switch_plot = Instance(Plot)

    distance_plot = Instance(Plot)

    pot_plot = Instance(Plot)

    link_plot = Instance(Component)

    plot_data = Instance(ArrayPlotData)

    line = Any()
    ax = Any()

    ### Outputs  ##############################################################

    led = Int(output=True)

    servo = Int(output=True)

    motor = Int(output=True)

    ### IOController Interface  ###############################################

    added_links = List()

    removed_links = List()

    outputs = Dict()

    ### Private Traits  #######################################################

    _current_links = Set()

    ### Trait Defaults  #######################################################

    def _logo_plot_default(self):
        fig = Figure()
        ax = Axes3D(fig)
        line, = ax.plot((1, 2), (1, 2), (1, 2))
        self.line = line
        self.ax = ax
        self.ax.set_xlim(0, 1, auto=False)
        self.ax.set_ylim(0, 1, auto=False)
        self.ax.set_zlim(0, 1, auto=False)
        return fig

    def _acc_x_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('acc_x',))
        plot.padding = (0, 0, 0, 0)
        plot.value_mapper.range.low_setting = 0
        plot.value_mapper.range.high_setting = 1
        return plot

    def _acc_y_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('acc_y',))
        plot.padding = (0, 0, 0, 0)
        plot.value_mapper.range.low_setting = 0
        plot.value_mapper.range.high_setting = 1
        return plot

    def _acc_z_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('acc_z',))
        plot.padding = (0, 0, 0, 0)
        plot.value_mapper.range.low_setting = 0
        plot.value_mapper.range.high_setting = 1
        return plot

    def _switch_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('switch',))
        plot.padding = (0, 0, 0, 0)
        plot.value_mapper.range.low_setting = 0
        plot.value_mapper.range.high_setting = 1
        return plot

    def _distance_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('distance',))
        plot.padding = (0, 0, 0, 0)
        plot.value_mapper.range.low_setting = 0
        plot.value_mapper.range.high_setting = 1
        return plot

    def _pot_plot_default(self):
        plot = Plot(self.plot_data)
        plot.plot(('potentiometer',))
        plot.padding = (0, 0, 0, 0)
        plot.value_mapper.range.low_setting = 0
        plot.value_mapper.range.high_setting = 1
        return plot

    def _link_plot_default(self):
        return LinksComponent()

    def _plot_data_default(self):
        plot_data = ArrayPlotData()
        plot_data.set_data('distance', np.zeros(50))
        plot_data.set_data('potentiometer', np.zeros(50))
        plot_data.set_data('switch', np.zeros(50))
        plot_data.set_data('acc_x', np.zeros(50))
        plot_data.set_data('acc_y', np.zeros(50))
        plot_data.set_data('acc_z', np.zeros(50))
        return plot_data

    def clicked(self, win):
        import ipdb
        ipdb.set_trace()  # XXX BREAKPOINT

    ### Trait Change Handlers  ################################################

    @on_trait_change('acc_x, acc_y, acc_z')
    def _update_3d_plot(self):
        if self.line and self.ax and self.ax.figure.canvas:
            x, y, z = self.acc_x, self.acc_y, self.acc_z
            #self.line.set_data(np.array([[0, 0, 0], [x, y, z]]).T)
            data = np.array([[.5, .5, .5], [x, y, z]]).T
            self.line.set_data(data[0:2, :])
            self.line.set_3d_properties(data[2, :])
            self.ax.figure.canvas.draw()
            #print x, y, z
            #self.ax.clear()
            #self.ax.plot((0, x), (0, y), (0, z))
            #self.ax.set_xlim(0, 1, auto=False)
            #self.ax.set_ylim(0, 1, auto=False)
            #self.ax.set_zlim(0, 1, auto=False)
            #self.ax.figure.canvas.draw()

    @on_trait_change('+plot_data')
    def _push_to_plot_data(self, name, new):
        # XXX This is causing NSConcreteMapTable to leak
        ary = self.plot_data[name]
        if ary is not None:
            ary = np.append(ary, new)
            ary = ary[-50:]
            self.plot_data.set_data(name, ary)

    @on_trait_change('+output')
    def _push_to_server(self, name, new):
        self.outputs[name] = new
        print self.outputs

    @on_trait_change('link_plot.links[]')
    def _links_changed(self, new):
        new = set(new)
        old = self._current_links
        added = new - old
        added_links = []
        for i, out in added:
            added_links.append((INPUT_MAP[i], OUTPUT_MAP[out]))
        removed = old - new
        removed_links = []
        for i, out in removed:
            removed_links.append((INPUT_MAP[i], OUTPUT_MAP[out]))
        self._current_links = new
        self.added_links.extend(added_links)
        self.removed_links.extend(removed_links)
        print added, removed
