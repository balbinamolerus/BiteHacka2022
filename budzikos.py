import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
from datetime import datetime, date

alarmPin = 4
clockAlarm = False
h = 0
min = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(alarmPin, GPIO.OUT)


def on_message(client, userdata, message):
    global direction, piren
    if message.topic == "alarm" and (
            str(message.payload.decode("utf-8")) == 'pir' or str(message.payload.decode("utf-8")) == 'door' or str(
            message.payload.decode("utf-8")) == 'knock'):
        warningAlarm()
    if message.topic == "alarmclock" and (str(message.payload.decode("utf-8")) == ''):
        clock()
    if message.topic == "alarmclock" and (str(message.payload.decode("utf-8")) == 'disaled'):
        stopAlarm()


def startAlarm():
    GPIO.output(alarmPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(alarmPin, GPIO.LOW)
    time.sleep(0.1)


def warningAlarm():
    for i in range(10)
        GPIO.output(alarmPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(alarmPin, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(alarmPin, GPIO.LOW)


def stopAlarm():
    global clockAlarm
    GPIO.output(alarmPin, GPIO.LOW)
    clockAlarm = False


def clock():
    global h, min, clockAlarm
    if clockAlarm:
        if (datetime.now().hour == h and datetime.now().minute == min):
            startAlarm()
        else:
            GPIO.output(alarmPin, GPIO.LOW)
            clockAlarm = False
