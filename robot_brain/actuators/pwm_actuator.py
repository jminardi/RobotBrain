import threading
import time

import RPi.GPIO as io


class PWMActuator(object):
    """
    Methods
    -------
    set(value)
        Use software PWM to output a value between 0 and 1

    Attributes
    ----------
    pin_number : int
    period : float
    value : float (0.0 - 1.0)

    """

    def __init__(self, pin_number, period=0.01, mode=io.BCM):
        """
        Parameters
        ----------

        pin_number : int
            number to use for this pin
        period : float
            period in seconds of the PWM cycle
        mode : int
            pin numbering scheme (see RPi.GPIO docs)

        """
        self.pin_number = pin_number  # Read Only
        self.period = period
        self.value = 0.0  # Read Only
        self.range(0, 1)
        self._thread = threading.Thread(target=self._worker)
        self._stopped = True

        io.setmode(mode)
        io.setup(pin_number, in_out)
        self._thread.start()

    def set(self, value):
        """
        Parameters
        ----------
        value : float
            Percentage of period to be outputing high
            (must be between 0 and 1)

        """

        if value > 1.0:
            value = 1.0
        elif value < 0.0:
            value = 0.0
        self.value = value

        if value == 0.0:
            self._stopped = True
            io.output(self.pin_number, io.LOW)
        elif value == 1.0:
            self._stopped = True
            io.output(self.pin_number, io.HIGH)
        else:
            self._stopped = False
            if not self._thread.is_alive():
                self._thread = threading.Thread(target=self._worker)
                self._thread.start()

    def set_normalized(self, value):
        self.set(value)

    def _worker(self):
        """worker method that is spawned in its own thread"""
        while not self._stopped:
            time_on = self.value * self.period
            time_off = (1 - self.value) * self.period

            io.output(self.pin_number, io.HIGH)
            time.sleep(time_on)

            io.output(self.pin_number, io.LOW)
            time.sleep(time_off)
        return
