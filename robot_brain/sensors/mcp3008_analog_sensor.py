import spidev

spi = spidev.SpiDev()
spi.open(0,0)


class MCP3008AnalogSensor(object):

    def __init__(self, channels, range=(0, 1023)):
        for chan_num in channels:
            if chan_num > 7 or chan_num < 0:
                raise ValueError('Valid channels on MCP3008 are 0-7')
        self.channels = channels
        self.num_values = len(channels)
        self.range = range

    def start(self):
        spi = spidev.SpiDev()
        spi.open(0, 0)

    def read(self):
        return [self._read_adc(chan) for chan in self.channels]

    def read_normalized(self):
        min, max = self.range
        return [(val - min) / float(max) for val in self.read()]

    def _read_adc(self, channel):
        """ Read SPI data from MCP3008 chip.
        """
        r = spi.xfer2([1, (8 + channel) << 4, 0])
        adc_value = ((r[1] & 3) << 8) + r[2]
        return adc_value
