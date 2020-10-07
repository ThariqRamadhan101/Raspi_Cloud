import time
import paho.mqtt.client as paho
broker = "maqiatto.com"

# create client object
client = paho.Client("P1")
client.username_pw_set("athariqramadhan@gmail.com", password="qwerty")
#####
print("connecting to broker ", broker)
client.connect(broker)  # connect
time.sleep(2)
print("publishing ")
client.publish("athariqramadhan@gmail.com/demo", "on")  # publish
time.sleep(4)
client.loop_forever()  # loop forever
