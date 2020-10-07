import paho.mqtt.client as mqtt
import time
import datetime


def on_message(mosq, obj, msg):
    if msg.topic == "receive":
        timestamp = datetime.datetime.now()
        filename = "receive_" + \
            timestamp.strftime("%d-%m-%Y_%H-%M-%S") + ".jpg"
        print("Received ", filename)
        with open('data/' + filename, 'wb') as fd:
            fd.write(msg.payload)


# Start MQTT Client
broker_address = "maqiatto.com"
client = mqtt.Client("P1")                                # Start MQTT Client
client.username_pw_set("athariqramadhan@gmail.com", password="qwerty")
client.connect(broker_address, 1883, 60)                 # Connect to server
client.subscribe("athariqramadhan@gmail.com/demo", 0)
client.on_message = on_message
client.loop_start()


while True:
    x = input("Request image? :")
    if x == "yes":
        print("publishing ")
        client.publish("athariqramadhan@gmail.com/send", "oi")  # publish
