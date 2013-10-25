import RPi.GPIO as io

from robot_brain.gpio_pin import GPIOPin


class Motor(object):
    
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        io.setmode(io.BCM)
        io.setup(pin1, io.OUT)
        io.setup(pin2, io.OUT)

        self.Pin1 = GPIOPin(pin1)
        self.Pin2 = GPIOPin(pin2)

    def drive_forward(self):
        io.output(self.pin1, io.HIGH)
        io.output(self.pin2, io.LOW)

    def drive_back(self):
        io.output(self.pin1, io.LOW)
        io.output(self.pin2, io.HIGH)

    def stop(self):
        io.output(self.pin1, io.LOW)
        io.output(self.pin2, io.LOW)

    def drive(self, speed=0.0):
        if speed >= 0.0:
            self.Pin1.output(speed)
            self.Pin2.output(0)
        else:
            self.Pin1.output(0)
            self.Pin2.output(abs(speed))
