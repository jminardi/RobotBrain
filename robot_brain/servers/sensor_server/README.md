This directory contains both the client and server components of a demo
application that uses the RobotBrain framework.

Basic Use
---------

Server Side (Raspberry Pi)
==========================
Start up the sensor server by launching python and creating a server instance.

    >>> from robot_brain.servers.sensor_server import SensorServer
    >>> s = SensorServer(port=2000)

Client Side
===========
On another computer with network access to the pi launch the client. The IP
should be the IP of the Pi, and the port should be the same as the port opened
on the Pi.

    python -m robot_brain.servers.sensor_server.sensor_client 192.168.1.80:2000
