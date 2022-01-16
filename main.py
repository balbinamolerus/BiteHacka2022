from cgitb import reset
import RPi.GPIO as GPIO
import time
from telegram import Telegram

global knock
global doors
doors = 0
door_open = 0
knock = 0
rreset_door = 0
rreset_knock = 0

#GPIO SETUP
channel = 17
channel_pir = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel_pir, GPIO.IN) 
def callback(channel):
        if GPIO.input(channel):
                print ('Sound Detected!')
                global knock
                knock += 1

        else:
                print ('Sound Detected!')
                global knock
                knock += 1

def callback_pir(channel_pir):
        if GPIO.input(channel_pir):
                print ('switch')
                global doors
                doors += 1
        else:
                print ('switch')
                global doors
                doors += 1


bocik = Telegram()

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=200)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
GPIO.add_event_detect(channel_pir, GPIO.BOTH, bouncetime=1000)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel_pir, callback_pir)  # assign function to GPIO PIN, Run function on change

while True:
    if doors > 5 & door_open == 0:
        door_open = 1
        print('The door was opened')
        bocik.msg_all('The door was opened')

    if knock > 1:
        print('knock knock')
        bocik.msg_all('knock knock')
    if rreset_door == doors:
        doors = 0
        door_open = 0
    if rreset_knock == knock:
        knock = 0
    rreset_knock = knock
    rreset_door = doors
    time.sleep(2)
