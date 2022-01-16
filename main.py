from cgitb import reset
import RPi.GPIO as GPIO
import time
from telegram import Telegram
import paho.mqtt.client as mqtt

global knock
global doors
doors = 0
door_open = 0
knock_turn = 0
knock = 0
rreset_door = 0
rreset_knock = 0

# alarm

#GPIO SETUP
channel = 17
channel_pir = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel_pir, GPIO.IN) 
def callback(channel):
    global knock
    print ('Sound Detected!')
    knock += 1

def callback_pir(channel_pir):
    global doors
    doors += 1


bocik = Telegram()

def on_message(client, userdata, message):
    global bocik
    bocik.msg_all('Alarm detected lmao')
    print("message received")


GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=200)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
GPIO.add_event_detect(channel_pir, GPIO.BOTH, bouncetime=1000)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel_pir, callback_pir)  # assign function to GPIO PIN, Run function on change

client = mqtt.Client()
client.on_message=on_message 
client.connect("192.168.0.123", 1881) 
client.loop_start() 
client.subscribe("alarm")

while True:
    if doors > 5 & door_open == 0:
        door_open = 1
        client.publish("alarm", "door", qos=0, retain=False)
        print('The door was opened')
        bocik.msg_all('The door was opened')

    if knock > 3 & knock_turn == 0:
        knock_turn = 1
        print('knock knock')
        client.publish("alarm", "knock", qos=0, retain=False)
        bocik.msg_all('knock knock')
    if rreset_door == doors:
        doors = 0
        door_open = 0
    if rreset_knock == knock:
        knock = 0
        knock_turn = 0
    rreset_knock = knock
    rreset_door = doors
    time.sleep(2)
