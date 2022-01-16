import paho.mqtt.client as mqtt
from gpiozero import MotionSensor
from gpiozero import Servo
import time

direction = 0
pir = MotionSensor(4)
servo = Servo(17)
servo.detach()
piren = False


def on_message(client, userdata, message):
    global direction, piren
    print(str(message.payload.decode("utf-8")))
    if message.topic == "position":
        # client.publish("test2", "ok", qos=0, retain=False)
        direction = int(message.payload.decode("utf-8"))
    elif message.topic == "alarm" and str(message.payload.decode("utf-8")) == "pir1":
        piren = True
        print(piren)
    elif message.topic == "alarm" and str(message.payload.decode("utf-8")) == "pir0":
        piren = False
        print(piren)


broker_address = "192.168.0.123"
client = mqtt.Client()
client.username_pw_set("Raspberry_Pi", "Rpi_Raspberry_Python")
client.on_message = on_message
client.connect(broker_address, 1881)
client.loop_start()
client.subscribe([("position", 0), ("alarm", 0)])



while True:
    motion = 0
    if direction == -1:
        piren = False
        servo.max()
        time.sleep(0.02)
        servo.detach()
        direction = 0
    elif direction == 1:
        piern = False
        servo.min()
        time.sleep(0.02)
        servo.detach()
        direction = 0
    if piren:
        for i in range(30):
            if pir.motion_detected:
                motion += 1
            time.sleep(0.01)
            if motion > 10:
                print('alarm')
                client.publish("alarm", "pir", qos=0, retain=False)
                time.sleep(2)
                break
