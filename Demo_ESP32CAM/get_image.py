import paho.mqtt.client as mqtt
import cv2
import numpy as np
import datetime

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("dimyog7@gmail.com/demo")

# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    print("Get image")
    timestamp = datetime.datetime.now()
    filename = "receive_" + timestamp.strftime("%d-%m-%Y_%H-%M-%S") + ".jpg"
    # image = np.asarray(bytearray(msg.payload), dty="uint8")
    image = np.frombuffer(msg.payload, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    try:
        cv2.imwrite("./data/" + filename, image)
        print("image saved")
    except:
        print("fail to save image")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("dimyog7@gmail.com", password="demoesp32")

client.connect("maqiatto.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
