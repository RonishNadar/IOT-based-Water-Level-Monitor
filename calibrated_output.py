# Importing the required modules for the script.
import os
import multiprocessing
import ultra_sonic
import loading

# Objects of ultrasonic.py and loading.py scripts.
sensor_cal = ultra_sonic.UltraSonic()
load = loading.LoadingScreen()

# Class for the calibration of the total capacity of the tank.
class CalibOut:
	def __init__(self):
		pass
	
	# When called the function writes the calibrated output data onto the CalibratedOutput.txt file.
	def cal_write(self):
		cwrite = open('CalibratedOutput.txt','w')
		sensor_cal.calib()
		cwrite.write(str(sensor_cal.calib()))
		cwrite.close()
	
	# When called the function displays the animated loading screen for calibration.
	def loadingLCD(self):
		load.loadingpercent()

# Class for running the calibration in the backend and
# display the loading screen in the frontend(LCD display).
class ParPro:
	def __init__(self):
		pass
		
	def parallelprocess(self):
		# Object of CalibOut class from above.
		calsave = CalibOut()
		
		# Defining two processes.
		p1 = multiprocessing.Process(target=calsave.loadingLCD)
		p2 = multiprocessing.Process(target=calsave.cal_write)
		
		# Starts and runs both processes parallelly.
		p1.start()
		p2.start()
		p1.join()
		p2.join()

# For testing this script alone.
if __name__=="__main__":
	parapros = ParPro()	
	if True:
		parapros.parallelprocess()
