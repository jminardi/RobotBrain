from robot_brain.actuators import PWMActuator


class MotorActuator(object):
    """ A Motor uses two PWM pins to drive a motor connected to an H-Bridge.

    Parameters
    ----------
    pin1 : int
        The forward pin connected to the H-Bridge motor control chip.
    pin2 : int
        The backward pin connected to the H-Bridge motor control chip.

    """

    def __init__(self, pin1, pin2):
        self.forward_pin = PWMActuator(pin1)
        self.backward_pin = PWMActuator(pin2)

    def drive_forward(self):
        self.forward_pin.set(1)
        self.backward_pin.set(0)

    def drive_back(self):
        self.forward_pin.set(0)
        self.backward_pin.set(1)

    def stop(self):
        self.forward_pin.set(0)
        self.backward_pin.set(0)

    def drive(self, speed=0.0):
        if speed == 0.0:
            self.stop()
        elif speed >= 0.0:
            self.forward_pin.set(speed)
            self.backward_pin.set(0)
        else:
            self.forward_pin.set(0)
            self.backward_pin.set(abs(speed))

    def set_normalized(self, val):
        speed = val * 2 - 1
        self.drive(speed=speed)
