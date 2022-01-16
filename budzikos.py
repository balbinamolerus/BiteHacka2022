import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
from datetime import datetime, date

alarmen = False
alarmtim = None
currAlarm = 0
alarmPin = 4
clockAlarm = False
h = 0
mn = 0

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
    if message.topic == "alarmclock" and (str(message.payload.decode("utf-8")) == 'disable'):
        clockAlarm = False


def startAlarm():
    GPIO.output(alarmPin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(alarmPin, GPIO.LOW)
    time.sleep(0.5)


def warningAlarm():
    for i in range(10):
        GPIO.output(alarmPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(alarmPin, GPIO.LOW)
        time.sleep(0.5)
    GPIO.output(alarmPin, GPIO.LOW)


def stopAlarm():
    GPIO.output(alarmPin, GPIO.LOW)


def clock():
    global h, min, clockAlarm



broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1881)
client.loop_start()
client.subscribe([("alarm", 0), ("alarmclock", 0)])

while True:
    if currAlarm:
        warningAlarm()
        currAlarm = 0
    if datetime.now().hour == alarmtim[0] and datetime.now().minute == alarmtim[1]:
        while clockAlarm:
            startAlarm()
        stopAlarm()
