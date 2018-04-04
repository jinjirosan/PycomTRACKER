import machine
import math
import network
import os
import time
import utime
import socket
import struct
import pycom
from network import Sigfox
from pytrack import Pytrack
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12

# init Sigfox for RCZ1 (Europe)
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
# create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
# make the socket blocking
s.setblocking(True)
# configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

datatosend = ("what up")
print('sigfox send: {}\n'.format(datatosend))
s.send(datatosend)
# pycom.rgbled(0x007f00)
# time.sleep(1.4)

py = Pytrack()
acc = LIS2HH12()
pitch = acc.pitch()
roll = acc.roll()
print('{},{}'.format(pitch,roll))
time.sleep_ms(100)

pycom.heartbeat(True)
