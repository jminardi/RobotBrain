import time
import json
import threading

import zmq

from robot_brain.sensors import MCP3007AnalogSensor, PingSensor
from robot_brain.actuators import PWMActuator, ServoActuator


class SensorServer(object):

    def __init__(self, port=2012):
        self.port = port

        # Whether or not to continue running the server
        self._run = True

        self.sensor_data = {}
        self.links = []

        self.start()

    def start(self):
        """ Initialize and start threads. """

        # Sensors
        self.acc = MCP3007AnalogSensor([0, 1, 2], range=(100, 800))
        self.pot = MCP3007AnalogSensor([3])
        self.switch = MCP3007AnalogSensor([4])
        self.ping = PingSensor(25, 24)

        # Actuators
        self.motor = PWMActuator(23)
        self.led = PWMActuator(18)
        self.servo = ServoActuator(0)
        self.actuators = {
                    'motor': self.motor,
                    'led': self.led,
                    'servo': self.servo,
                }

        self._server_thread = threading.Thread(target=self._server_worker)
        self._server_thread.start()

        self._sensor_thread = threading.Thread(target=self._read_worker)
        self._sensor_thread.start()

        self._link_thread = threading.Thread(target=self._link_worker)
        self._link_thread.start()

    def stop(self):
        """ Shut down server and control threads. """
        self._run = False
        print 'joining threads'
        self._server_thread.join()
        self._sensor_thread.join()
        self._link_thread.join()
        print 'threads were joined'

    def _server_worker(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:{}".format(self.port))
        print 'bound to socket:', socket

        while self._run:
            time.sleep(.1)
            #  Wait for next request from client
            message = socket.recv()
            if len(message) > 2:
                print "Received request: ", message

            request = json.loads(message)
            self._handle_request(request)

            #  Send current sensor values back to client
            socket.send(json.dumps(self.sensor_data))
        socket.close()

    def _read_worker(self):
        while self._run:
                # read the analog pins
                x_val, y_val, z_val = self.acc.read_normalized()
                pot_val, = self.pot.read_normalized()
                switch_val, = self.switch.read_normalized()
                ping_val, = self.ping.read_normalized()
                self.sensor_data['acc_x'] = x_val
                self.sensor_data['acc_y'] = y_val
                self.sensor_data['acc_z'] = z_val
                self.sensor_data['potentiometer'] = pot_val
                self.sensor_data['distance'] = ping_val
                self.sensor_data['switch'] = switch_val
                time.sleep(0.1)

    def _link_worker(self):
        while self._run:
            for in_, out in self.links:
                actuator = self.actuators[out]
                sensor_value = self.sensor_data[in_[0]]
                actuator.set_normalized(sensor_value)
            time.sleep(0.1)

    def _handle_request(self, request):
        if 'out' in request:
            out = request['out']
            for actuator_name, value in out.iteritems():
                value = value / 100.0  # XXX should normalized on client side.
                actuator = self.actuators[actuator_name]
                actuator.set_normalized(value)
        if 'add_link' in request:
            print '!link set to:', request['add_link']
            self.links.extend(request['add_link'])
        if 'remove_link' in request:
            print '!link removed:', request['remove_link']
            for link in request['remove_link']:
                self.links.remove(link)
