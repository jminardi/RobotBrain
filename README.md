RobotBrain
==========
RobotBrain is a framework that makes it easy to work with sensors and actuators
on the Raspberry Pi.

Actuators
---------
    
All Actuator objects implement a `set_normalized()` method which takes a value
between 0 and 1 as input.

__Currently Implemented Actuators:__

* `Motor` (Software PWM controlled DC motor)
* `ServoActuator`
* `PWMActuator`

The following code is all that is needed to set an attached
servo to it's center postion:

    >>> from robot_brain.actuators import ServoAcuator
    >>> s = ServoActuator(servod_path='</path/to/servod-executable>')
    >>> s.set_normalized(0.5)
    
Sensors
-------

All Sensor objects implement a `read_normalized()` method which returns the
sensor's current reading normalized to be between 0 and 1.

__Currently Implemented Sensors:__

* `PingSensor` (HC-SR04)
* `MCP3008AnalogSensor` (ADC chip for reading analog sensors)

Dependencies
------------
* RPi.GPIO
    + (Most OSs come preinstalled with this)

* spidev
    ```
    git clone git://github.com/doceme/py-spidev                                       
    sudo python setup.py install  
    ```

* PiBits
    + PiBits is used to drive servos 

    ```
    git clone https://github.com/richardghirst/PiBits                                 
    cd PiBits/ServoBlaster/user                                                              
    # edit out pins that are not needed in servod.c
    make servod  
    ```

* ZMQ
    ```
    sudo apt-get install python-zmq
    ```

Installation
------------
```
sudo python setup.py install
```


TODO
----
* [x] Make `Motor` confirm to the Actuator Interface
* [ ] Update Pin tests
* [ ] Add more tests!
