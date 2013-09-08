import socket
import threading
import time

from motor import Motor
from servo import Servo


class CarServer(object):

    def __init__(self, motor_pins=(24, 25), servo_pin=0, port=2012):
        self.port = port

        # The motor and servo for driving
        self.motor = Motor(*motor_pins)
        self.servo = Servo(servo_pin)
        
        # The most recent coordinates from the accelerameter
        self.coords = (0, 0, 0)

        # Whether or not to continue running the server
        self._run = True

        self.start()

    def start(self):
        """ Initialize and start threads. """

        self._server_thread = threading.Thread(target=self._server_worker)
        self._server_thread.start()
        self._control_thread = threading.Thread(target=self._control_worker)
        self._control_thread.start()

    def stop(self):
        """ Shut down server and control threads. """
        self._run = False

    def _server_worker(self):
        HOST = ''  # Symbolic name meaning all available interfaces
        PORT = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        conn, addr = s.accept()

        print 'Connected by', addr
        while self._run:
            data = conn.recv(1024)
            if data:
                coords = data[1:].split(',')
                x, y, z = [float(n) for n in coords]
                self.coords = (x, y, z)
            conn.sendall(data)
        conn.close()

    def _control_worker(self):
        while self._run:
            x, y, z = self.coords
            forward_speed = -y/10
            turning_power = (x+10)/20

            self.motor.drive(forward_speed)
            self.servo.set(turning_power)
