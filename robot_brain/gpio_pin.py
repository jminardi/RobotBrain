import RPi.GPIO as io


class GPIOPin(object):

    def __init__(self, pin_number, mode=io.BCM, in_out=io.OUT):
        """
        Parameters
        ----------
        pin_number : int
            number to use for this pin
        mode : int
            pin numbering scheme (see RPi.GPIO docs)
        in_out : int
            whether this pin will be an input (1) or output (0)

        """
        self.pin_number = pin_number  # Read Only
        self.range = (0, 1)

        io.setmode(mode)
        io.setup(pin_number, in_out)
        io.output(self.pin_number, io.LOW)

    def set(self, value):
        """
        Parameters
        ----------
        value : int (0 or 1)

        """

        io.output(self.pin_number, value)

    def set_normalized(self, value):
        if value >= 0.5:
            self.set(1)
        elif value < 0.5:
            self.set(0)

    def get(self):
        return io.input(self.pin_number)

    def get_normalized(self):
        return self.get()
