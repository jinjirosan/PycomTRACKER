import machine
import time
from network import WLAN
import wlanconfig

# setup WLAN
wlan = WLAN(mode=WLAN.STA)  # get current object, without changing the mode

# if machine.reset_cause() != machine.SOFT_RESET:
#     wlan.init(mode=WLAN.STA)
#     # configuration below MUST match your home router settings!!
#     wlan.ifconfig(config=(wlanconfig.airmax_ip, wlanconfig.airmax_subnet, wlanconfig.airmax_gateway, wlanconfig.airmax_ns)
#
# if not wlan.isconnected():
#     # change the line below to match your network ssid, security and password
#     wlan.connect(wlanconfig.airmax_ssid, auth=(WLAN.WPA2, wlanconfig.airmax_key), timeout=5000)
# while not wlan.isconnected():
#     machine.idle()  # save power while waiting

def do_connect():
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)       # activate the interface
    if not wlan.isconnected():      # check if the station is connected to an AP
        wlan.connect(wlanconfig.airmax_ssid, auth=(WLAN.WPA2, wlanconfig.airmax_key), timeout=5000)  # connect to the AP (Router)
        for _ in range(10):
            if wlan.isconnected():      # check if the station is connected to an AP
                wlan.ifconfig(config=(wlanconfig.airmax_ip, wlanconfig.airmax_subnet, wlanconfig.airmax_gateway, wlanconfig.airmax_ns)
                break
            print('.', end='')
            time.sleep(1)
        else:
            print("Connect attempt timed out\n")
            return
    print('\nnetwork config:', wlan.ifconfig())
