import json
import sys
import threading

import enaml
import zmq

from io_controller import IOController


class SensorApp(object):

    #def __init__(self, ip='192.168.43.48', port=2019):
    def __init__(self, ip='192.168.1.80', port=2024):
        self.ip = ip
        self.port = port

        self._run = True

        self.io_controller = IOController()

        self.start()

    def start(self):
        self._sensor_client_thread = threading.Thread(
                target=self._sensor_client_worker)
        self._sensor_client_thread.start()

    def stop(self):
        self._run = False

    def _sensor_client_worker(self):
        ## XXX Mock sensor values
        #import numpy as np
        #while self._run:
        #    updates = {'acc_x': int(np.random.random() * 1024),
        #                   'acc_y': int(np.random.random() * 1024),
        #                   'acc_z': int(np.random.random() * 1024),
        #                   'switch': np.random.random() * 360,
        #                   'distance': np.random.random() * 90,
        #                   'potentiometer': np.random.random()}
        #    self.io_controller.set(**updates)
        #    import time
        #    time.sleep(.1)

        context = zmq.Context()

        #  Socket to talk to server
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://{}:{}".format(self.ip, self.port))

        while self._run:
            send = {}
            if self.io_controller.added_links:
                add = self.io_controller.added_links
                self.io_controller.added_links = []
                send['add_link'] = add
            if self.io_controller.removed_links:
                remove = self.io_controller.removed_links
                self.io_controller.removed_links = []
                send['remove_link'] = remove
            if self.io_controller.outputs:
                outputs = self.io_controller.outputs
                self.io_controller.outputs = {}
                send['out'] = outputs
            socket.send(json.dumps(send))
            message = socket.recv()
            self.io_controller.set(**json.loads(message))
        socket.close()


if __name__ == '__main__':
    from enaml.stdlib.sessions import show_simple_view
    with enaml.imports():
        from sensor_view import SensorViewWindow
    ip, port = sys.argv[1].split(':')
    sensor_app = SensorApp(ip=ip, port=port)
    window = SensorViewWindow(io_controller=sensor_app.io_controller)
    show_simple_view(window)
    sensor_app.stop()
