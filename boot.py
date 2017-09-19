import machine
from network import WLAN
import wlanconfig

# setup WLAN
wlan = WLAN()  # get current object, without changing the mode

if machine.reset_cause() != machine.SOFT_RESET:
    wlan.init(mode=WLAN.STA)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(config=(wlanconfig.airmax_ip, wlanconfig.airmax_subnet, wlanconfig.airmax_gateway, wlanconfig.airmax_ns)

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect(wlanconfig.airmax_ssid, auth=(WLAN.WPA2, wlanconfig.airmax_key), timeout=5000)
    while not wlan.isconnected():
        machine.idle() # save power while waiting
