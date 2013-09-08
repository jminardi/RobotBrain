This is a simple python package written to remotely control a toy car. It was
developed on and written for the Raspbery Pi.

Starting the Server
-------------------
    >> from robot_brain.servers.car_server import CarServer
    >> server = CarServer()

Stopping the Server
-------------------
    >> server.stop()

More Information
----------------
The server listens on the port specified when it is instantiated (default 2012).
Data streaming into the server should be of the form: ":x,y,x" where x, y and z
are the values read in from an accelerometer.

The DC motor and servo motor pins are also specified at server instantiation
(default (24, 25) and 0 respectively)

To start a server that listens on port 2000 with a servo connected to pin 1 and
a DC motor connected to pins 18 and 24:

    >> server = CarServer(motor_pins=(18, 24), servo_pin=1, port=2000)

See Also
--------
The client side Android software that communicates with this server:

https://github.com/jminardi/RobotBrain-Controller
