import cv2
import numpy as np
import face_recognition
import csv
from datetime import datetime

known_faces_folder = "known_faces"
attendance_file = "attendance.csv"

def recognize_faces():
    # Load known faces from known_faces_folder
    known_face_encodings = []
    known_face_names = []
    for file in os.listdir(known_faces_folder):
        image = face_recognition.load_image_file(os.path.join(known_faces_folder, file))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(file.split('.')[0])

    # Open camera stream
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Find all faces in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Iterate over each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if this face matches any of the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If we found a match, use the first one
            if True in matches:
                index = matches.index(True)
                name = known_face_names[index]

            # Draw a rectangle around the face and label it with the person's name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Write the name and time to the attendance file
            with open(attendance_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Wait for 'q' key to be pressed to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    video_capture.release()
    cv2.destroyAllWindows()

if _name_ == '_main_':
    recognize_faces()
