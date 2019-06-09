import cv2
import sys
import time
import threading

from face import facefinder
from camera import VideoCamera
from flask import Flask, render_template, Response

video_camera = VideoCamera(flip=False)
object_classifier = cv2.CascadeClassifier("model/facial_recognition_model.xml")


app = Flask(__name__)
last_epoch = 0

def check_for_objects():
        global last_epoch
        while True:
                try:
                        frame, found_obj = video_camera.get_object(object_classifier)
                        if found_obj and (time.time() - last_epoch) > 2:
                                last_epoch = time.time()
                                facefinder(video_camera.get_frame())
                except:
                        print ("Error finding_face: "), sys.exc_info()[0]

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
