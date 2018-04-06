import time
import machine
import pycom
import adxl345

pycom.heartbeat(False)

#Set the I2C and Pin to machine. so the code from before still works
I2C = machine.I2C
Pin = machine.Pin
Timer = machine.Timer

chrono = Timer.Chrono()

#initialize the I2C bus
i2c = I2C(0, I2C.MASTER, baudrate=100000)

value = 0

time.sleep_ms(1000)
setRTCLocalTime()

savedTime = time.localtime()
counter = 1
timeThreshold = 600

#threshold is measued in g
threshold = 1
stateMotion = False
hitCount = 0
stateSigfox = False
measureCounter = 500
measureThreshold = 500

#Set this to false to turn off indication lights
lightVar = True

if lightVar == True:
	print('Turn lights on')

chrono.start()
print('Starting the loop')

while True:
	data = adxl345.ADXL345(i2c)
	axes = data.getAxes(True)
	x = axes['x']
	x = abs(x)
	y = axes['y']
	y = abs(y)
	z = axes['z']
	z = abs(z)
	measureCounter += 1
	if (threshold <= x) or (threshold <= y) or (threshold <= z):
		if measureThreshold <= measureCounter:
			stateMotion = True
			hitCount = hitCount + 1
			print('I have been hitten')
			print('My count is ')
			print(hitCount)
			measureCounter = 0
	#This function checks if it is allowed to send a message via SigFox (one every 10 minutes)
	if  timeThreshold <= chrono.read():
		stateSigfox = True
		chrono.stop()
	#This function first checks if the state of motion has changed, ie. have the acc crossed the threshold
	if stateMotion == True:
		#Then it checks if it is allowed to send a message
		if stateSigfox == True:
			#Send shit to sigfox
			print('I am going to send this hit count ')
			print(hitCount)
			# Send the bitcount to SigFox
			hitCount = str(hitCount)
			s.send("Hit" + hitCount)
			counter = 1
			stateSigfox = False
			stateMotion = False
			hitCount = 0
			chrono.reset()
			chrono.start()
	if lightVar == True:
		if (stateMotion == True) and (stateSigfox != True):
			#There has been motion but SigFox is not allowed to send messages
			pycom.rgbled(0x007f00) #green
		elif (stateMotion != True) and (stateSigfox == True):
			#Sigfox can send message but there has been no motion
			pycom.rgbled(0x7f7f00) #yellow
		elif (stateMotion != True) and (stateSigfox != True):
			#Neither motion has occured or SigFox can send messages
			pycom.rgbled(0x7f0000) #red
