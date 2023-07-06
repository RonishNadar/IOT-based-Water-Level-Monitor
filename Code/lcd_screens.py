# Importing the required modules for the script.
import time
import drivers

# Object of LCD display driver.
display = drivers.Lcd()

# Class for display the options screen for the program.
class LcdScreens:
	
	def __init__(self):
		pass
	# When called the function displays the corresponding strings on the 16x2 LCD.
	def first_screen(self):
		display.lcd_display_string("1.CALIBRATION   ", 1)
		display.lcd_display_string("2.TANK LEVEL    ", 2)

# For testing this script alone.
if __name__=="__main__":
	screen = LcdScreens()
	while True:
		screen.first_screen()
		time.sleep(1)