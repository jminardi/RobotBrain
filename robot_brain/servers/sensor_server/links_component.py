import numpy as np
from numpy.linalg import norm
from traits.api import Int, List, Property
from enable.api import Component


N_INPUTS = 6
N_OUTPUTS = 3


def is_close_to_one(number, tolerence=.001):
    return True if abs(1 - number) < tolerence else False


class LinksComponent(Component):

    # List of tuples of the form: (input_index, output_index)
    links = Property(List(), depends_on='_output_indexes[]', cached=True)

    # Distance from edge to draw the endpoints
    b = Int(30)

    # Radius of the endpoints
    r = Int(15)

    # List of lines to draw
    lines = List()

    # List of current input indexes
    _input_indexes = List()

    # List of current output indexes
    _output_indexes = List()

    bgcolor = (0.9294, 0.9294, 0.9294)

    def draw(self, gc, **kwargs):
        super(LinksComponent, self).draw(gc, **kwargs)
        with gc:
            self._draw_endpoints(gc)
            self._draw_lines(gc)
        return

    def _draw_endpoints(self, gc):
        self.w, self.h = w, h = gc.width(), gc.height()
        gc.set_stroke_color((0.145, 0.2, 0.439, 1))
        gc.set_line_width(4.0)
        r = self.r
        b = self.b
        s = h / 13
        self.left_circle_pos = lcp = np.linspace(s, h - s, N_INPUTS)
        self.right_circle_pos = rcp = lcp[:N_OUTPUTS]
        for y_coord in lcp:
            gc.arc(b, y_coord, r, 0, 360)
        for y_coord in rcp:
            gc.arc(w - b, y_coord, r, 0, 360)
        gc.stroke_path()

    def _draw_lines(self, gc):
        w, h = gc.width(), gc.height()
        gc.set_line_width(4.0)
        gc.set_stroke_color((0.675, 0.686, 0.702, 1))
        for line in self.lines:
            x1, y1, x2, y2 = line
            gc.move_to(x1, y1)
            gc.line_to(x2, y2)
        gc.stroke_path()

    ### 'normal' Event State Handlers  ########################################

    def normal_key_pressed(self, event):
        print "key pressed: ", event.character

    def normal_left_down(self, event):
        circle_y, i = self._get_nearest_circle(event.x, event.y)
        # if we hit an input circle, start a new link line
        if circle_y is not None:
            self.lines.append([self.b, circle_y, event.x, event.y])
            self._input_indexes.append(i)
            self.event_state = 'connecting'
            event.handled = True
            self.request_redraw()
        else:  # if we didn't git a circle, see if we hit a line then remove it
            clicked_line_index = self._get_nearest_line(event.x, event.y)
            if clicked_line_index is not None:
                self.lines.pop(clicked_line_index)
                self._input_indexes.pop(clicked_line_index)
                self._output_indexes.pop(clicked_line_index)
                self.request_redraw()

    ### 'connecting' Event State Handlers  ####################################

    def connecting_left_down(self, event):
        circle_y, i = self._get_nearest_circle(event.x, event.y)
        if circle_y:
            self.lines[-1][2:] = [self.w - self.b, circle_y]
            self._output_indexes.append(i)
        else:
            self.lines.pop()
        self.event_state = 'normal'
        event.handled = True
        self.request_redraw()

    def connecting_mouse_move(self, event):
        self.lines[-1][-2:] = [event.x, event.y]
        event.handled = True
        self.request_redraw()

    ### Property getters  #####################################################

    def _get_links(self):
        links = zip(self._input_indexes, self._output_indexes)
        return links

    ### Private methods  ######################################################

    def _get_nearest_circle(self, x, y):
        """ Returns the nearest circle and index or None.
        """
        if self.event_state == 'normal':  # only check input circles
            left_gutter = self.b + self.r
            if x > left_gutter:  # border + radius
                return None, 0
            for i, circle_y in enumerate(self.left_circle_pos):
                if circle_y - self.r < y and circle_y + self.r > y:
                    return circle_y, i
            return None, 0

        if self.event_state == 'connecting':  # only check output cirlces
            right_gutter = self.w - (self.b + self.r)
            if x < right_gutter:
                return None, 0
            for i, circle_y in enumerate(self.right_circle_pos):
                if circle_y - self.r < y and circle_y + self.r > y:
                    return circle_y, i
            return None, 0

    def _get_nearest_line(self, x, y):
        """ Returns the nearest line index, or None.
        """

        if not (self.b + self.r < x < self.w - self.b):  # In a gutter
            return None

        for i, line in enumerate(self.lines):
            # Check to see if a line drawns from each lines start point is
            # parallel to that line. If it is, then we hit the line.
            orig_x, orig_y = line[:2]
            line_x, line_y = line[2:]
            line = np.array([line_x - orig_x, line_y - orig_y])
            click = np.array([x - orig_x, y - orig_y])
            angle = np.dot(line, click) / norm(line) / norm(click)
            if is_close_to_one(angle):
                return i
