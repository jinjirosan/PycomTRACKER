from machine import UART
import machine
import time
import os
from network import WLAN
from network import Sigfox
import pycom
import binascii
import socket
import wlanconfig

known_nets = [('wlanconfig.airmax_ssid', 'wlanconfig.airmax_key')]

# Initiates Sigfox communicationn
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)  # RCZ1/RCZ3 Europe / Japan / Korea

# Initiates the UART (USB) connection
uart = machine.UART(0, 115200)
os.dupterm(uart)

# setup WLAN
wlan = WLAN(mode=WLAN.STA)  # get current object, without changing the mode
wlan_timeout = time.time() + 15
pycom.heartbeat(False)
pycom.rgbled(0x090000)

if not wlan.isconnected():
    #wlan = network.WLAN(network.STA_IF)  # create station interface
    #wlan.active(True)       # activate the interface
    #wlan.ifconfig(config=(wlanconfig.airmax_ip, wlanconfig.airmax_subnet, wlanconfig.airmax_gateway, wlanconfig.airmax_ns))
    wlan.ifconfig(config=('dhcp'))
    wlan.scan()     # scan for available networks
    wlan.connect(wlanconfig.airmax_ssid, auth=(WLAN.WPA2, wlanconfig.airmax_key), timeout=5000)  # connect to the AP (Router)
colors = [0x000009, 0x000900, 0x090000]

while not wlan.isconnected() and time.time() < wlan_timeout:
        pycom.rgbled(colors[time.time() % len(colors)])
        time.sleep(1)

try:
    # print(">> boot.py: IP: {:,}".format(wlan.ifconfig()[0]))
    print('\nnetwork config:', wlan.ifconfig())  # print full wifi info
except:
    pass

# SigFox setup
# -> Create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
# -> Make the socket blocking
s.setblocking(True)
# -> Configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

# Time setup
def setRTCLocalTime():
    rtc = machine.RTC()
    rtc.ntp_sync("pool.ntp.org")
    time.sleep_ms(750)
    print('\nRTC Set from NTP to UTC', rtc.now())
    time.timezone(3600)  # GMT + 1 Copenhagen, Amsterdan, Paris
    print('Adjusted from UTC to GMT+1', time.localtime(), '\n')


pycom.heartbeat(False)

machine.main('main.py')
print('==========Starting main.py==========\n')
