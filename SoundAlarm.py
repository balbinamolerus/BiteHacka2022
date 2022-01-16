import numpy as np
import sounddevice as sd
import paho.mqtt.client as mqtt
import datetime

broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi_Hat", "Rpi_Raspberry_Python_Sound_Sensor")

def audio_callback(indata, frames, time, status):
   global client
   volume_norm = np.linalg.norm(indata) * 10
   if volume_norm > 700:
      client.publish(f'[{(datetime.datetime.today()).strftime("%H:%M:%S")}] LoundNoise', 'Alarm', qos=0, retain=False) 
      # print(f'[{(datetime.datetime.today()).strftime("%H:%M:%S")}] Published')

client.connect(broker_address, 1881)
stream = sd.InputStream(callback=audio_callback)
with stream:
   print('Loop started')
   client.loop_forever()