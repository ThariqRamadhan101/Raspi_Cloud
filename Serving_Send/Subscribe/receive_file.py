import paho.mqtt.client as mqtt
import time
import datetime

# Function to retrieve file when received


def on_message(mosq, obj, msg):
    timestamp = datetime.datetime.now()
    filename = "receive_" + timestamp.strftime("%d-%m-%Y_%H-%M-%S") + ".jpg"
    print("Received ", filename)
    with open('data/' + filename, 'wb') as fd:
        fd.write(msg.payload)


# Start MQTT Client, NB changed to P2
broker_address = "maqiatto.com"
client = mqtt.Client("P2")                                # Start MQTT Client
client.username_pw_set("athariqramadhan@gmail.com", password="qwerty")
client.connect(broker_address, 1883, 60)                 # Connect to server
client.subscribe("athariqramadhan@gmail.com/demo", 0)

# This is key - it calls the function
client.on_message = on_message

while True:                                               # Loop and wait for next image
    client.loop(20)
