# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
from flask import request, redirect
import threading
import argparse
import datetime
import imutils
import time
import cv2
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    time.sleep(1)
    # For Text
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


broker_address = "maqiatto.com"
client = mqtt.Client("P2")                                # Start MQTT Client
client.username_pw_set("athariqramadhan@gmail.com", password="qwerty")
client.subscribe("athariqramadhan@gmail.com/send")
client.on_message = on_message
client.connect(broker_address, 1883, 60)                 # Connect to server
client.loop_start()
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
# vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)


@app.route("/")
def index():
    # return the rendered template
    client.loop()
    return render_template("index.html")


def stream_camera(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock

    # loop over frames from the video stream
    while True:

        # read the next frame from the video stream, resize it,
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()

        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 50),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
              bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/upload', methods=['POST'])
def upload():

    global outputFrame, lock
    with lock:
        timestamp = datetime.datetime.now()
        filename = "send_" + timestamp.strftime("%d-%m-%Y_%H-%M-%S") + ".jpg"
        cv2.imwrite("./upload/" + filename, outputFrame)
    file = open("upload/" + filename, "rb")
    # read the file
    imagestring = file.read()
    # convert to byte string
    byteArray = bytes(imagestring)
    client.publish(topic="athariqramadhan@gmail.com/demo", payload=byteArray,
                   qos=0)  # publish it to the MQ queue
    return redirect('/')


# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, default='0.0.0.0',
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, default="8000",
                    help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
                    help="# of frames used to construct the background model")
    args = vars(ap.parse_args())

    # start a thread that will perform stream camera
    t = threading.Thread(target=stream_camera, args=(
        args["frame_count"],))
    t.daemon = True
    t.start()

    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()
