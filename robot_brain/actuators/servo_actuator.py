import os

SERVOD_PATH='/home/pi/Code/theirs/PiBits/ServoBlaster/user/servod'


class ServoActuator(object):
    """A Servo instance controls a single servo

    Parameters
    ----------
    pin : int
        GPIO pin number the servo is connected to
    min : int
        Minimun pulse width (in 10s of us) servo responds to
    max : int
        Maximum pulse width (in 10s of us) servo responds to
    servod_path : str
        Path to the "servod" executable

    """

    def __init__(self, pin=0, range=(70, 230), servod_path=SERVOD_PATH):
        self.pin = pin
        self.range = range
        self.servod_path = servod_path
        
        if not self._servoblaster_started():
            self.start()

    def set(self, pulse_width):
        """
        Parameters
        ----------
        pulse_width : int
            pulse width to send to the servo measured in 10s of us
        """
        os.system('echo "{}={}" > /dev/servoblaster'.format(self.pin,
                                                            pulse_width))

    def set_normalized(self, val):
        min, max = self.range
        scale = max - min
        speed = min + int(val * scale)
        self.set(speed)

    def start(self):
        os.system('sudo {}'.format(self.servod_path))

    def stop(self):
        servod_name = os.path.split(self.servod_path)[1]
        os.system('sudo killall {}'.format(servod_name))

    def _servoblaster_started(self):
        servod_name = os.path.split(self.servod_path)[1]
        return servod_name in os.popen('ps -u root').read()
