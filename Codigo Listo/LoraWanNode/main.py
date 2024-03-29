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

py = Pysense()
si = SI7006A20(py)
mpp = MPL3115A2(py,mode=PRESSURE)

#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from network import LoRa
import socket
import binascii
import struct
import time
import config

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('2601147D'))[0]
nwk_swkey = binascii.unhexlify('3C74F4F40CAEA021303BC24284FCF3AF')
app_swkey = binascii.unhexlify('0FFA7072CC6FF69A102A0F39BEB0880F')

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# set the 3 default channels to the same frequency
lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

for i in range (200):
    degC = si.temperature()
    presion = mpp.pressure()
    humedad = si.humidity()
    rssi = lora.stats()
    pkt = b'PKT #' + bytearray(struct.pack("f", degC)) + b' PKT #' + bytearray(struct.pack("f", presion)) + b' PKT #' + bytearray(struct.pack("f", humedad))
   #  pkt = b'PKT #' + bytes([i])

   #  degC = si.temperature()
   #  raw = bytearray(struct.pack("f", degC))
    # print("t", degC, "p", presion, "h", humedad, "rssi", rssi)
    print("t", degC, "p", presion, "h", humedad)
    print('Sending:', pkt)
    s.send(pkt)
    time.sleep(4)
    rx, port = s.recvfrom(256)
    if rx:
        print('Received: {}, on port: {}'.format(rx, port))
    time.sleep(6)





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