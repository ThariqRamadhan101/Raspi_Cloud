import paho.mqtt.client as mqtt
import time

broker_address = "maqiatto.com"
client = mqtt.Client("P1")                                # Start MQTT Client
client.username_pw_set("athariqramadhan@gmail.com", password="qwerty")
client.connect(broker_address, 1883, 60)                 # Connect to server

# initial start before loop
client.loop_start()

while True:
    # open the file, note r = read, b = binary
    file = open("send.jpg", "rb")
    # read the file
    imagestring = file.read()
    # convert to byte string
    byteArray = bytes(imagestring)
    client.publish(topic="athariqramadhan@gmail.com/demo", payload=byteArray,
                   qos=0)  # publish it to the MQ queue
    time.sleep(20)
