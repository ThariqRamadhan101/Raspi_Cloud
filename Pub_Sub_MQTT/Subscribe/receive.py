import time
import paho.mqtt.client as paho
broker = "maqiatto.com"
# define callback


def on_message(client, userdata, message):
    time.sleep(1)
    # For Text
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


# create client object
client = paho.Client("P2")
# Bind function to callback
client.username_pw_set("athariqramadhan@gmail.com", password="qwerty")
client.on_message = on_message
#####
print("connecting to broker ", broker, 1883, 60)
client.connect(broker)  # connect
print("subscribing ")
client.subscribe("athariqramadhan@gmail.com/demo")  # subscribe
time.sleep(2)
client.loop_forever()  # loop forever
