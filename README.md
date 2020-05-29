# PycomTRACKER

## (a.k.a. BabyCarriageMonitor 3.0)

This is the third release of the same idea. See: <https://github.com/jinjirosan/BabyCarriageMonitor>

The goal is to use the features of the previous platform and make it more energy efficient in a smaller form-factor. More compact and portable.

I've chosen the PyCom SiPy with Pytrack board as the new platform.

## Communication

This specific chip can communicate on three transmitters: Bluetooth, WiFi and Sigfox.

- Sigfox will be used as primary, outside of known wifi locations (e.g. home). Data tx needs to be efficient and compressed to to message limitations (size & interval)
- WiFi will be used on known locations to send all local logging and as means to determine longer-term stationary positions (e.g. turn off GPS/GLONASS power)
- Bluetooth is optional but the idea is to use it as remote control to enable/disable tracker functions.

## GPS/GLONASS

The platform supports GPS, GLONASS, Galileo and QZSS so will have to make good use of this to get the most accurate reading.
Activation of location services will be A) when known WiFi is no longer detected or B) motion-detection from the 3-axis accelerometer.

## Power management

The Pytrack board has a 1S LiPo charger built-in (awesome!) which I'll hook up to a 1S 3.7V 1200mAh battery.

<< insert measurements table >>

## Frozen Modules

As this generation of SiPy has limited memory available and some libraries are more extensive I've opted for the frozen module option on the MicroPython platfom. This basically means you bake the library into the firmware. That's why you see a reference to trackerlogger.py but it is not in the /lib.

## Kanban

See <https://github.com/jinjirosan/PycomTRACKER/projects/1?>

## Credits

I'm building on the excellent work done by the Pycom team, Pycom library makers such as the standard L76GNSS.py, the MicropyGPS module and KarlBunch's pytrack-poller.
Thx to Markus Jünemann for the excellent writeup on frozen modules on the Pycom platform.
