# Importing the required modules for the script.
import  RPi.GPIO as GPIO
import time

# Setting the GPIO mode of Raspberry Pi to BOARD.
GPIO.setmode(GPIO.BOARD)

# Defining the pins for trigger and echo pins of the HC-SR04 sensor.
trig_pin = 10
echo_pin =12

# Setting the trigger as output and echo as input.
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Class for the functions of the ultrasonic sensor.
class UltraSonic:
	def __init__(self):
		pass
	# When called the function calculates the distance in cm and 
	# percentage of water level and returns them.
	def ultra(self):
		# Set Trigger to HIGH.
		GPIO.output(trig_pin, True)
		# Set Trigger after 0.01ms to LOW.
		time.sleep(0.00001)
		GPIO.output(trig_pin, False)

		startTime = time.time()
		stopTime = time.time()

		# Save the start time.
		while 0 == GPIO.input(echo_pin):
			startTime = time.time()

		# Save the time of arrival.
		while 1 == GPIO.input(echo_pin):
			stopTime = time.time()

		# Time difference between start and arrival.
		TimeElapsed = stopTime - startTime
		# Multiplying with the sonic speed (34300 cm/s)
		# and dividing by 2, because there and back.
		distance = (TimeElapsed * 34300) / 2
		time.sleep(0.5)
		print ("Distance: %.1f cm" % distance)
		# Uses the max capacity set by the calib function
		# to calculate the relative percentage of water.
		tankread = open('CalibratedOutput.txt', 'r')
		tankcap = tankread.readlines()
		tankread.close()
		capacity = ''.join(map(str,tankcap))
		capacity = float(capacity)
		perc = (distance/capacity)*100
		perc = 100-perc
		time.sleep(0.5)
		return distance, perc
	
	# When called the function sets the max capacity of the tank
	# by taking 10 consecutive inputs from the sensor
	# (For this process the tank has to be empty)
	# and returns the average to set the capacity.
	def calib(self):
		tank_capacity = 0
		for i in range(10):	
			# Set Trigger to HIGH.
			GPIO.output(trig_pin, True)
			# Set Trigger after 0.01ms to LOW.
			time.sleep(0.00001)
			GPIO.output(trig_pin, False)

			startTime = time.time()
			stopTime = time.time()

			# Save the start time.
			while 0 == GPIO.input(echo_pin):
				startTime = time.time()

			# Save the time of arrival.
			while 1 == GPIO.input(echo_pin):
				stopTime = time.time()
	
			# Time difference between start and arrival.
			TimeElapsed = stopTime - startTime
			# Multiplying with the sonic speed (34300 cm/s)
			# and dividing by 2, because there and back.
			distance = (TimeElapsed * 34300) / 2
			time.sleep(0.5)
			tank_capacity += distance
		return tank_capacity/10

# For testing this script alone.
if __name__=="__main__":
	sensor = UltraSonic()
	while True:
		print(sensor.ultra())
		time.sleep(0.5)
