#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics

# Import what is necessary to create a thread

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

import _thread
from time import sleep

py = Pysense()

# Increment index used to scan each point from vector sensors_data
def inc(index, vector):
    if index < len(vector)-1:
        return index+1
    else:
        return 0

# Define your thread's behaviour, here it's a loop sending sensors data every 5 seconds
def send_env_data():
    idx = 0
    mpp = MPL3115A2(py,mode=PRESSURE)
    si = SI7006A20(py)
    sensors_data = [str(mpp.pressure()),str(si.temperature()),str(si.humidity())]


    while True:
        # send one element from array `sensors_data` as signal 1
        pybytes.send_signal(1, str(mpp.pressure()))
        pybytes.send_signal(2, str(si.temperature()))
        pybytes.send_signal(3, str(si.humidity()))
        print("Presión: " + str(mpp.pressure()))
        print("Temperatura: " + str(si.temperature())+ " [°C] ")
        print("Humedad: " + str(si.humidity()) + " % ")
        sleep(5)


# Start your thread
_thread.start_new_thread(send_env_data, ())




 # print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

 # print("Battery voltage: " + str(py.read_battery_voltage()))
# pycom.rgbled(0x7f7f00)

# import pycom
# import time

# pycom.heartbeat(False)
# for cycles in range(5): # stop after 5 cycles
#     pycom.rgbled(0x007f00) # green
#     time.sleep(5)
#     pycom.rgbled(0x7f7f00) # yellow
#     time.sleep(1.5)
#     pycom.rgbled(0x7f0000) # red
#     time.sleep(4)
�޶ӝ