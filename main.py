import cv2
import sys
import time
import threading

from camera import VideoCamera
from face import detectPersonen
from flask_basicauth import BasicAuth
from flask import Flask, render_template, Response

video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically

# App Globals
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'CHANGE_ME_USERNAME'
app.config['BASIC_AUTH_PASSWORD'] = 'CHANGE_ME_PLEASE'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0

def check_for_objects():
	global last_epoch
	while True:
		try:
			frame, found_obj = video_camera.get_object(cv2.CascadeClassifier("facial_recognition_model.xml"))
			if found_obj and (time.time() - last_epoch) > 600:
				last_epoch = time.time()
				#############
				#detectPersonen(frame)
				#############
		except:
			print ("Error face_recognition: "), sys.exc_info()[0]

@app.route('/')
@basic_auth.required
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
