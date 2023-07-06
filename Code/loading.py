# Importing the required modules for the script.
import drivers
import time

# Objects of LCD display driver.
mylcd = drivers.Lcd()

# Class for display the animated loading screen.
class LoadingScreen:
     def __init__(self):
          pass
     
     # When called the function displays the respective bit data on the 16x2 LCD screen.  
     def loadingpercent(self):
          fontdata1 = [
                  [ 0b00000,
                    0b00000, 
                    0b01110, 
                    0b01110, 
                    0b01110, 
                    0b00000, 
                    0b00000, 
                    0b00000 ]
          ]
     
          mylcd.lcd_clear()
          
          mylcd.lcd_display_string("LOADING:", 1)

          mylcd.lcd_load_custom_chars(fontdata1)

          mylcd.lcd_write(0xC0)

          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)
          mylcd.lcd_write_char(0)
          time.sleep(1)

# For testing this script alone.
if __name__=="__main__":
	load = LoadingScreen()
	while True:
          load.loading()
