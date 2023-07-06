# Importing the required modules for the script.
import paho.mqtt.client as mqtt
import time
import lcd_screens
import ultra_sonic
import drivers
import calibrated_output
import RPi.GPIO as GPIO

# Objects of the respective scripts.
screen = lcd_screens.LcdScreens()
sensor = ultra_sonic.UltraSonic()
display = drivers.Lcd()
parapros = calibrated_output.ParPro()

# Setting the GPIO mode of Raspberry Pi to BOARD.
GPIO.setmode(GPIO.BOARD)

# Defining the pin for motor state.
motor_pin = 37
# Setting the motor as output and default as off.
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.output(motor_pin, GPIO.LOW)

# When called this function displays the options screen.
def initial_screen():
    screen.first_screen()
    time.sleep(1)

# When called this function calls the ultrasonic function
# and controls the motor state.
def waterlevel():
    dist_level, perc_level = sensor.ultra()
    print(dist_level)
    # Displays the distance on the screen.
    display.lcd_display_string("Distance:%.1fcm" % dist_level + "     ", 1)
    print(perc_level)
    # Displays the percentage on the screen.
    display.lcd_display_string("Percent:%.1f" % perc_level + "%" + "     ", 2)
    
    # Updates the current percentage of water level
    # and writes onto the CurrentPercentData.txt file.
    percdata = open('CurrentPercentData.txt','w')
    percdata.write(str(round(perc_level,1)))
    percdata.close()
    
    # When the water level reaches below 20% the motor is turned on.
    if (perc_level >= 0 and perc_level < 20):
        GPIO.output(motor_pin, GPIO.HIGH)
        status = "Low"
        print(status)

    # When the water level reaches above 80% the motor is turned off.
    if (perc_level >= 80 and perc_level < 100):
        GPIO.output(motor_pin, GPIO.LOW)
        status = "High"
        print(status)

# When called the funtion does the calibration process i.e. sets the max capacity of the tank.
def calbdone():
    parapros.parallelprocess()
    display.lcd_display_string("Calibration Done" + "             ", 1)
    display.lcd_display_string("                                  ", 2)
    time.sleep(2)
    initial_screen()

##########Defining all call back functions###################

# The callback for when the client connects to the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# The callback for when a PUBLISH message is received from the server.
def on_message(client,userdata,message):
    global msg
    msg = str(message.payload.decode("utf-8"))
    print(str(message.topic),msg)
    SWITCH = 0

    # When the message payload is 'cal' calbdone() is called.
    if msg == "cal":
        calbdone()

    # When the message payload is 'cal' calbdone() is called.
    while msg == "wat":
        waterlevel()

# Called when the broker responds to a subscribe request.
def on_subscribe(client, userdata,mid,granted_qos):
    print("Subscribed:", str(mid),str(granted_qos))

# Called when the client disconnects from the broker.
def on_disconnect(client,userdata,rc):
    if rc !=0:
       print("Unexpected Disconnection")

# Address and port of the Broker(Raspberry Pi).
broker_address = "192.168.1.28"
port = 1883

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Entering the username and password of the client.
client.username_pw_set("iotwaterlevel", "ronish14")
# Connecting to the respective address and port.
client.connect(broker_address,port)

# Displaying the options screen.
initial_screen()

time.sleep(1)

# Subscribing topic of the client.
subtop = "/iot/sub"

# Subscribes to the subtop topic.
client.subscribe(subtop)

# Loops the process forever until terminated.
client.loop_forever()