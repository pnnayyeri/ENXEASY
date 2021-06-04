from ENXEASY import Encoder
import RPi.GPIO as GPIO

encoder = Encoder(17,27).start()

try:
	while True:
		print("{0:4d}".format(encoder.read_pos()))
				
except KeyboardInterrupt:
	print("cleaning up GPIO")
	GPIO.cleanup()
