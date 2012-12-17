#! /bin/bash

DIR=$( cd "$( dirname "$0" )" && pwd )
insmod $DIR/servoblaster.ko num_servos=4
major=$( sed -n 's/ servoblaster//p' /proc/devices )
mknod -m 0666 /dev/servoblaster c $major 0
exit 0
