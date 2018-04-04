import machine
import time
from network import WLAN
import wlanconfig

# setup WLAN
wlan = WLAN(mode=WLAN.STA)  # get current object, without changing the mode

#wlan = network.WLAN(network.STA_IF)  # create station interface
#wlan.active(True)       # activate the interface
wlan.ifconfig(config=(wlanconfig.airmax_ip, wlanconfig.airmax_subnet, wlanconfig.airmax_gateway, wlanconfig.airmax_ns))
wlan.scan()     # scan for available networks
wlan.connect(wlanconfig.airmax_ssid, auth=(WLAN.WPA2, wlanconfig.airmax_key), timeout=5000)  # connect to the AP (Router)
print('\nnetwork config:', wlan.ifconfig())
