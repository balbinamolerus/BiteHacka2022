from time import sleep
import paho.mqtt.client as mqtt
from gpiozero import MotionSensor
from gpiozero import Servo


pir = MotionSensor(4)
servo = Servo(17)

def on_message(client, userdata, message):
    global servo
    if message.topic == "position":
        # client.publish("test2", "ok", qos=0, retain=False)
        pos = int(message.payload.decode("utf-8"))
        servo.value = (pos/50)-1


broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1881)
client.loop_start()
client.subscribe([("position", 0), ])


while True:
    motion = 0
    for i in range(30):
        if pir.wait_for_motion() == True:
            motion += 1
        sleep(0.01)
        if motion > 10:
            # print('alarm')
            client.publish("alarm", "pir", qos=0, retain=False)
            sleep(2)
            break