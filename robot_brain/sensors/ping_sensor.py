import RPi.GPIO as io


class PingSensor(object):

    def __init__(self, trigger, echo, range=(0, 100)):
        self.trigger = trigger
        self.echo = echo
        self.range = range
        self.num_values = 1

        io.setup(trigger, io.OUT)
        io.setup(echo, io.IN)

    def read(self):
        # Send 10us pulse to trigger
        io.output(self.trigger, True)
        time.sleep(0.00001)
        io.output(self.trigger, False)

        start = time.time()
        while io.input(self.echo) == 0:
            # Wait for echo to go high
            stop = time.time()
            if (stop - start) > .1:
                break

        start = time.time()
        while io.input(self.echo) == 1:
            # wait for echo to go low
            stop = time.time()
            if (stop - start) > .1:
                break

        # Calculate pulse length
        elapsed = stop - start

        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        distance = elapsed * 34300

        # That was the distance there and back so halve the value
        distance = distance / 2

        # Cap value at 100
        if distance > 100:
        distance = 100

        return distance,

    def read_normalized(self):
        value = self.read()[0] / float(self.range[1])
        return value,
