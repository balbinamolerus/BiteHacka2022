import RPi.GPIO as GPIO
import time
#GPIO SETUP
channel = 17
channel_pir = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel_pir, GPIO.IN) 
def callback(channel):
        if GPIO.input(channel):
                print ('Sound Detected!')
        else:
                print ('Sound Detected!')

def callback_pir(channel_pir):
        if GPIO.input(channel_pir):
                print ('switch')
        else:
                print ('switch')

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
GPIO.add_event_detect(channel_pir, GPIO.BOTH, bouncetime=1000)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel_pir, callback_pir)  # assign function to GPIO PIN, Run function on change

# infinite loop
while True:
    time.sleep(1)
