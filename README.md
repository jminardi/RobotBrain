RobotBrain
----------
RobotBrain is a framework that makes it easy to work with sensors and actuators
on the Raspberry Pi.

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
    cd ServoBlaster/user                                                              
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
* [ ] Make `Motor` confirm to the Actuator Interface
* [ ] Allow passing of command line arguments to `sensor_client`
* [ ] Update Pin tests
* [ ] Add more tests!
