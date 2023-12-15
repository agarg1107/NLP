import cv2
import face_recognition as fr
import numpy as np
import os
import pickle  # Added import for pickle
from datetime import datetime
import time
import serial
from Computer import speak
import subprocess
import Computer
try:
    s = serial.Serial('COM5', 9600)
except:
    print("error")

# Load known faces and encodings
def data(names):
    with open('datafile.csv', 'r+') as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])

        if names not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{names},{dtstring}')

# Function to save known faces and encodings to a file
def save_known_faces(known_faces, image_names, filename='known_faces.pkl'):
    data = {'known_faces': known_faces, 'image_names': image_names}
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

# Function to load known faces and encodings from a file
def load_known_faces(filename='known_faces.pkl'):
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            return data['known_faces'], data['image_names']
    except FileNotFoundError:
        return [], []

# Initialize video capture
cap = cv2.VideoCapture(0)

# Load or encode known faces and encodings
known_faces, image_names = load_known_faces()

if not known_faces:
    print("No pre-encoded data found. Encoding faces...")
    image_dir = 'D:/facerecpython/images'
    known_faces = []
    image_names = []

    for image_file in os.listdir(image_dir):
        if image_file.endswith(".jpg") or image_file.endswith(".png"):
            image_path = os.path.join(image_dir, image_file)
            image = fr.load_image_file(image_path)
            face_encoding = fr.face_encodings(image)
            if face_encoding:
                known_faces.append(face_encoding[0])
                image_names.append(os.path.splitext(image_file)[0].upper())

    # Save the encodings for future use
    save_known_faces(known_faces, image_names)
    print("Face encoding complete. Encodings saved.")

# Frame processing parameters
frame_count = 0  # Initialize frame count
recognized = False  # Flag to track if a face has been recognized
start_time = time.time()  # Initialize start time
main_id = "def"

max_time = 40
while not recognized and time.time() - start_time < max_time:
    ret, frame = cap.read()
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame from the camera.")
        break
    # Skip frames to improve performance
    if frame_count % 2 == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = fr.face_locations(rgb_small_frame)
        face_encodings = fr.face_encodings(rgb_small_frame, face_locations)

        for face_location, face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_faces, face_encoding)
            face_distances = fr.face_distance(known_faces, face_encoding)

            if True in matches:
                best_match_index = np.argmin(face_distances)
                name = image_names[best_match_index]

                top, right, bottom, left = [i * 2 for i in face_location]  # Scale back up
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
                # Record the data
                data(name)
                main_id = name

                recognized = True  # Set the recognized flag to stop

        cv2.imshow("WebCam", frame)

    frame_count += 1

    if cv2.waitKey(1) == 27 or (recognized and time.time() - start_time >= 5):  # Press 'Esc' key or after 2 seconds
        break

cap.release()
cv2.destroyAllWindows()
if(recognized == True):
    s.write(bytes('3', 'utf-8'))
    s.write(bytes('6', 'utf-8'))
    s.close()
    
    target_script_path = "jarvis.py"
    print(main_id)
    speak("Welcome "+main_id)
    if main_id == "AMAN":
        subprocess.run(["python", target_script_path, "1"])
    elif main_id == "AKSHIT":
        subprocess.run(["python", target_script_path, "2"])
    else:
        print("id not recognize")
        subprocess.run(["python", target_script_path, "0"])


else:
    print("not identified")