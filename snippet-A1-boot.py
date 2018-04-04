known_nets = [('ssid', 'pass')]

import machine
import os
from network import Sigfox
import binascii
import socket
import time

#Initiates Sigfox communication
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1) #RCZ1/RCZ3 Europe / Japan / Korea

#initiates the UART (USB) connection
uart = machine.UART(0, 115200)
os.dupterm(uart)

#WiFi setup
if machine.reset_cause() != machine.SOFT_RESET: #needed to avoid losing connection after a soft reboot
	from network import WLAN
	wl = WLAN()

	# save the default ssid and auth
	original_ssid = wl.ssid()
	original_auth = wl.auth()

	wl.mode(WLAN.STA)

	available_nets = wl.scan()
	nets = frozenset([e.ssid for e in available_nets])

	known_nets_names = frozenset([e[0] for e in known_nets])
	net_to_use = list(nets & known_nets_names)

	try:
		net_to_use = net_to_use[0]
		pwd = dict(known_nets) [net_to_use]
		sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
		wl.connect(net_to_use, (sec, pwd), timeout=10000)
	except:
		wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)

#SigFox setup

#Create a Sigfox socket
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
#Make the socket blocking
s.setblocking(True)
#Configure it as uplink only
s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)

#Time setup
def setRTCLocalTime():
	rtc = machine.RTC()
	rtc.ntp_sync("pool.ntp.org")
	time.sleep_ms(750)
	print('\nRTC Set from NTP to UTC', rtc.now())
	time.timezone(3600) #GMT + 1 Copenhagen, Amsterdan, Paris
	print('Adjusted from UTC to GMT+1', time.localtime(), '\n')
