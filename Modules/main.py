import cv2
import sys
import time
import imutils
import threading
import numpy as np
import face_recognition
from flask import Flask, render_template, Response
from imutils.video.pivideostream import PiVideoStream

video_capture = PiVideoStream().start()
time.sleep(2.0)

p1 = face_recognition.load_image_file("pictures/p1.jpg")
p1_face_encoding = face_recognition.face_encodings(p1)[0]

p2 = face_recognition.load_image_file("pictures/p2.jpg")
p2_face_encoding = face_recognition.face_encodings(p2)[0]

known_face_encodings = [
    p1_face_encoding,
    p2_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Novak Dokovic"
]

last_epoch = 0
face_locations = []
face_encodings = []
classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")

app = Flask(__name__)

def get_object():
        found_objects = False
        frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(objects) > 0:
            found_objects = True

        return (frame, found_objects)

def check_for_objects():
        global last_epoch
        while True:
                frame, found_obj = get_object()
                if found_obj and (time.time() - last_epoch) > 5:
                        last_epoch = time.time()
                        
                        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_small_frame = small_frame[:, :, ::-1]
                        
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                        for face_encoding in face_encodings:
                                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                                name = "Unknown"

                                if True in matches:
                                        first_match_index = matches.index(True)
                                        name = known_face_names[first_match_index]
                                print (name)
                        
@app.route('/')
def index():
    return render_template('index.html')

def get_frame():
        image = video_capture.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
