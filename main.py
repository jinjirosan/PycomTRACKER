# /usr/bin/env python
#
# Maintainer 	: JinjiroSan
# Version	: PycomTRACKER 0.5 - Sigfox_streamer - rewrite 0.1.3

import machine
import math
import network
import os
import time
import utime
import socket
import struct
import trackerlogger
from network import Sigfox
from machine import RTC
from machine import SD
from machine import Timer
from pytrack import Pytrack

# setup as a station
import gc

time.sleep(2)
gc.enable()
init_timer = time.time()

# setup vars
py = Pytrack()
poller = trackerlogger.GPS_Poller(json_output=True)
chrono = Timer.Chrono()
chrono.start()
# sd = SD()  # put boot.py SD card routine here when needed
# os.mount(sd, '/sd')
# f = open('/sd/gps-record.txt', 'w')

# initial GPS_Poller run (cold start)
poller.run()  # when GPS fix is obtained, values stored in trackerlogger.log_entry need to be fetched in main.py

while(True):
    # time-counter configurations
    final_timer = time.time()
    diff = final_timer - init_timer
    # save the coordinates in a new variable
    coord =   # find a way to get latitude-longitude from trackerlogger in coord variable once GPS fix is obtained
    #coord = (43.345543, 7.890123)  # test coords instead of waiting for fix
    # verify the coordinates received
    if coord == (None, None):  # ensure GPS_Poller outputs None,None when no GPS fix (or better yet, trigger on GPS Fix value!)
        poller.run()
        print("Getting Location...")
        continue

    # SigFox time wait (max 1 msg/10 mins)
    # diff <= 600 takes 10 min approximately to send the next message. Use 10 for testing.
    if diff <= 10 and coord != (None, None):
        print("Waiting to send the next Sigfox message")
        continue
    # write coords to sd card  # not sure if needed as trackerlogger does this too
    # f.write("{} - {}\n".format(coord, rtc.now()))  # save coords SD card

    # send the Coordinates to Sigfox
    s.send(struct.pack("<f", float(coord[0])) + struct.pack("<f", float(coord[1])))  # rewrite struct depending on coord
    print(struct.pack("<f", float(coord[0])) + struct.pack("<f", float(coord[1])))  # temp to see what s.send transmits
    print("Coordinates sent -> lat: " + str(coord[0]) + ", lng: " + str(coord[1]))
    # reset the timer
    time.sleep(5)
    init_timer = final_timer
