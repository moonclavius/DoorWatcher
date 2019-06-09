import cv2
import numpy as np
import face_recognition

p1 = face_recognition.load_image_file("p1.jpg")
p1_face_encoding = face_recognition.face_encodings(p1)[0]

p2 = face_recognition.load_image_file("p2.jpg")
p2_face_encoding = face_recognition.face_encodings(p2)[0]

known_face_encodings = [
    p1_face_encoding,
    p2_face_encoding
]
known_face_names = [
    "Person_1",
    "Person_2"
]

face_locations = []
face_encodings = []
face_names = []

def facefinder(frame):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
        	name = known_face_names[best_match_index]
        	print (name)

        face_names.append(name)
