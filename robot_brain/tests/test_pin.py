import unittest
import RPi.GPIO as io
from pin import Pin


class TestPin(unittest.TestCase):

    def setUp(self):
        pass

    def test_intitialization(self):
        p24 = Pin(24)
        self.assertEqual(p24.pin_number, 24)
        self.assertEqual(p24.period, 10e-3)
        self.assertEqual(p24.value, 0.0)
        self.assertTrue(p24._stopped)

    def test_output(self):
        p24 = Pin(24)
        p24.output(.5)
        self.assertEqual(p24.value, 0.5)

    def test_thread_running(self):
        p24 = Pin(24)
        p24.output(.5)
        self.assertTrue(p24._thread.is_alive())

    def test_output_zero(self):
        p24 = Pin(24)
        p24.output(0)
        self.assertEqual(p24.value, 0.0)
        self.assertTrue(p24._stopped)

    def test_output_one(self):
        p24 = Pin(24)
        p24.output(1)
        self.assertEqual(p24.value, 1.0)
        self.assertTrue(p24._stopped)

    def teardown(self):
        io.cleanup()


if __name__ == '__main__':
        unittest.main()
