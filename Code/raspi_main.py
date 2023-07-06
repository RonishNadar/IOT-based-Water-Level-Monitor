# Importing the required modules for the script.
import paho.mqtt.client as mqtt
import time
import sys
import subprocess
import drivers

# Object of the LCD driver scripts.
display = drivers.Lcd()

# Starting the mqtt_client.py script as a subprocess.
p = subprocess.Popen(['python3','mqtt_client.py'])

# When called the function terminates the subprocess
# and exits the current program i.e. closes everything.
def stop_process():
    p.terminate()
    display.lcd_clear()
    display.lcd_display_string("PROCESS", 1)
    display.lcd_display_string("ENDED", 2)
    time.sleep(2)
    display.lcd_clear()
    sys.exit(0)

# The callback for when the client connects to the broker.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    # Subscribes  to iotstop client.
    client.subscribe("iotstop")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client,userdata,message):
    msg = str(message.payload.decode("utf-8"))
    print(str(message.topic),msg)
    
    # When the message payload is 'stop' stop_process() is called.
    if msg == "stop":
        print('STOP')
        stop_process()
        
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Entering the username and password of the client.
client.username_pw_set("iotwaterlevel", "ronish14")
# Connecting to the respective address and port of the broker.
client.connect('192.168.1.28', 1883)

# Loops the process forever until terminated.
client.loop_start()
while True:
    # Reads the percentage data from CurrentPercentData.txt file,
    # rounds the value, converts to string and publish it to the
    # iotsub22 topic which displays the current percentage of the
    # water level.
    percdata = open('CurrentPercentData.txt','r')
    round_perc = (round(float(percdata.read()),1))
    disp_perc = str(round_perc) + '%'
    percdata.close()
    client.publish("iotsub22", disp_perc)
    time.sleep(0.5)
client.loop_stop()
