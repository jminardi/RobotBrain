import os

HERE = os.path.dirname(__file__)


class Servo(object):
    """A Servo instance controls a single servo

    Parameters
    ----------
    pin : int
        GPIO pin number the servo is connected to. With ServoBlaster module
        valid numbers are 0-3
    min : int
        Minimun value servo responds to (0-255)
    max : int
        Maximum value servo responds to (0-255)

    """

    def __init__(self, pin=0, min=70, max=230):
        self.pin = pin
        self.min = min
        self.max = max
        
        if not self._servoblaster_module_loaded():
            self._load_servoblaster()

    def set(self, position):
        """
        Parameters
        ----------
        position : float (between 0 and 1)
            Percentage of operational range to set servo at
            0: minimum position, 1: maximum position

        """
        range = self.max - self.min
        speed = self.min + int(position * range)
        os.system('echo "{}={}" > /dev/servoblaster'.format(self.pin, speed))

    def _servoblaster_module_loaded(self):
        return 'servoblaster' in os.popen('lsmod').read()

    def _load_servoblaster(self):
        loadscript = os.path.join(HERE, '../ServoBlaster/load.sh')
        os.system(loadscript)

    def _unload_servoblaster(self):
        unloadscript = os.path.join(HERE, '../ServoBlaster/unload.sh')
        os.system(unloadscript)
