from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
GPIO.setup(14, GPIO.IN)
while True:
    if GPIO.input(25):
        print('ruch')