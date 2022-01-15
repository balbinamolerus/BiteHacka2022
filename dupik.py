from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)

GPIO.output(4, 0)

GPIO.setup(4, GPIO.IN)
while True:
    if GPIO.input(14):
        print('ruch')