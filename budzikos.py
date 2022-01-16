import RPi.GPIO as GPIO
import time
from datetime import datetime, date
import numpy as np
import sounddevice as sd
import paho.mqtt.client as mqtt

# import datetime


alarmen = False
alarmtim = ('0', '0')
currAlarm = 0
alarmPin = 4
clockAlarm = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(alarmPin, GPIO.OUT)


def on_message(client, userdata, message):
    global currAlarm, clockAlarm, alarmtim
    if message.topic == "alarm" and (
            str(message.payload.decode("utf-8")) == 'pir' or str(message.payload.decode("utf-8")) == 'door' or str(
        message.payload.decode("utf-8")) == 'knock'):
        currAlarm = 1

    if message.topic == "alarmclock" and ',' in str(message.payload.decode("utf-8")):
        clockAlarm = True
        alarmtim = (str(message.payload.decode("utf-8"))[:2], str(message.payload.decode("utf-8"))[3:])
        print(alarmtim)
    if message.topic == "alarmclock" and (str(message.payload.decode("utf-8")) == 'disable'):
        clockAlarm = False


def startAlarm():
    GPIO.output(alarmPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(alarmPin, GPIO.LOW)
    time.sleep(0.1)


def warningAlarm():
    for i in range(5):
        GPIO.output(alarmPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(alarmPin, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(alarmPin, GPIO.HIGH)


def bigAlarm():
    for i in range(5):
        GPIO.output(alarmPin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(alarmPin, GPIO.LOW)
        time.sleep(0.2)
    GPIO.output(alarmPin, GPIO.HIGH)


def stopAlarm():
    GPIO.output(alarmPin, GPIO.HIGH)


def clock():
    global h, min, clockAlarm


def audio_callback(indata, frames, time, status):
    global client, currAlarm
    volume_norm = np.linalg.norm(indata) * 10
    print(volume_norm)
    if volume_norm > 700:
        print("boo")
        client.publish('LoundNoise', 'Alarm', qos=0, retain=False)
        currAlarm = 2
        # print(f'[{(datetime.datetime.today()).strftime("%H:%M:%S")}] Published')


broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1881)
client.loop_start()
client.subscribe([("alarm", 0), ("alarmclock", 0)])
stream = sd.InputStream(callback=audio_callback)
with stream:
    while True:
        time.sleep(1)
        # print(datetime.now().hour, datetime.now().minute, int(alarmtim[0]), int(alarmtim[1]))
        if currAlarm == 1:
            warningAlarm()
            currAlarm = 0
        elif currAlarm == 2:
            bigAlarm()
            currAlarm = 0
        if datetime.now().hour == int(alarmtim[0]) and datetime.now().minute == int(alarmtim[1]):
            while clockAlarm:
                startAlarm()
            stopAlarm()
