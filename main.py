import machine
import math
import network
import os
import time
import utime
import socket
import struct
from network import Sigfox
from machine import RTC
from machine import SD
from machine import Timer
from L76GNSS import L76GNSS
from pytrack import Pytrack

# setup as a station
import gc

time.sleep(2)
gc.enable()
init_timer = time.time()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')
py = Pytrack()
l76 = L76GNSS(py, timeout=30)
chrono = Timer.Chrono()
chrono.start()
sd = SD()
os.mount(sd, '/sd')
f = open('/sd/gps-record.txt', 'w')

while(True):
    # time-counter configurations
    final_timer = time.time()
    diff = final_timer - init_timer
    # save the coordinates in a new variable
    coord = l76.coordinates()
    #coord = (43.345543, 7.890123)  # test coords instead of waiting for fix
    # verify the coordinates received
    if coord == (None, None):
        print("Getting Location...")
        continue
    # time established to send the next Sigfox message
    # diff <= 600 takes 10 min approximately to send the next message
    if diff <= 10 and coord != (None, None):
        print("Waiting for send the next Sigfox message")
        continue
    # write coords to sd card
    f.write("{} - {}\n".format(coord, rtc.now()))  # save coords SD card
    # send the Coordinates to Sigfox
    #s.send(struct.pack("<f", float(coord[0])) + struct.pack("<f", float(coord[1])))
    print(struct.pack("<f", float(coord[0])) + struct.pack("<f", float(coord[1])))  # temp to see what s.send transmits
    print("Coordinates sent -> lat: " + str(coord[0]) + ", lng: " + str(coord[1]))
    # reset the timer
    time.sleep(5)
    init_timer = final_timer
