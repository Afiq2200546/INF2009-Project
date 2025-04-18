import os
import cv2
import time
import pickle
import numpy as np
import json
import face_recognition
import paho.mqtt.client as mqtt
from imutils import paths
from datetime import datetime, date
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from modules.ultrasonic import get_distance

# ------------------ Database Setup ------------------
INSTANCE_FOLDER = os.path.join(os.getcwd(), "instance")
os.makedirs(INSTANCE_FOLDER, exist_ok=True)
DATABASE_PATH = os.path.join(INSTANCE_FOLDER, "database.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = "user"  # Ensure this matches your table name
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    schedule_link = Column(String(300), nullable=False)  # Added schedule_link field

# ------------------ Face Recognition Setup ------------------
UPLOAD_FOLDER = '/home/pg14/Desktop/web_interface_2/Users'
ENCODINGS_FILE = "encodings.pickle"

def recognize_face():
    """
    Use the camera to detect and recognize a face.
    Returns the recognized username if found, otherwise returns None.
    """
    print("[INFO] Loading face recognition model...")
    if not os.path.exists(ENCODINGS_FILE):
        print("[ERROR] No trained model found. Please train the model first!")
        return None

    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.loads(f.read())

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open camera!")
        return None

    print("[INFO] Looking for a face...")
    max_attempts = 100
    attempts = 0

    while attempts < max_attempts:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(data["encodings"], face_encoding)
            face_distances = face_recognition.face_distance(data["encodings"], face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = data["names"][best_match_index]
                print(f"[INFO] Recognized: {name}")
                cap.release()
                return name
        attempts += 1

    cap.release()
    print("[INFO] Face not recognized within maximum attempts.")
    return None

def calculate_age(born):
    """
    Calculate age from the date of birth.
    """
    today = date.today()
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    return age

# ------------------ MQTT Publisher ------------------
def main():
    # Create MQTT client using the specified Callback API version.
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Publisher")
    client.connect("192.168.153.1", 1883)
    client.loop_start()

    age = None
    message_data = None
    message = None
    recognized_user = None
    distance = None
    try:
        while True:
            distance = get_distance()
            print(str(distance) + "sadasdasdasd")
            if distance <= 50.0:
                print("[INFO] Starting continuous face detection until a valid user is detected...")
                recognized_name = recognize_face()
                user = session.query(User).filter_by(name=recognized_name).first()
                # recognized_user = user

                if user:
                    recognized_user = user
                    age = calculate_age(recognized_user.date_of_birth)
                    message_data = {
                        "username": recognized_user.name,
                        "age": age,
                        "schedule_link": recognized_user.schedule_link  # Include schedule_link in the message
                    }
                    message = json.dumps(message_data)
                    print(f"[INFO] Valid user detected: {recognized_user.name}, Age: {age}. Starting continuous MQTT publishing...")

            if age is not None and message_data is not None and message is not None and recognized_user is not None:
                # client.publish("face/recognized", message)
                client.publish("name", recognized_user.name)
                client.publish("age", age)
                client.publish("schedule", recognized_user.schedule_link)
                client.publish("greet", "Hello, " + recognized_user.name + "!")
                print(f"[INFO] Published message: {message}")
                time.sleep(5)  # Publish every 5 seconds
    except KeyboardInterrupt:
        print("\n[INFO] Terminated by user.")
    finally:
        client.disconnect()

    # while not recognized_user:
    #     recognized_name = recognize_face()
    #     if not recognized_name:
    #         print("[INFO] No face recognized. Retrying...")
    #         continue

    #     user = session.query(User).filter_by(name=recognized_name).first()
    #     if not user:
    #         print("[INFO] Recognized user not found in the database. Retrying...")
    #         continue

    #     recognized_user = user

    # Once a valid user is detected, calculate age and create the MQTT message.
    
    

    # try:
    #     while True:
    #         # client.publish("face/recognized", message)
    #         client.publish("name", recognized_user.name)
    #         client.publish("age", age)
    #         client.publish("schedule", recognized_user.schedule_link)
    #         client.publish("greet", "Hello, " + recognized_user.name + "!")
    #         print(f"[INFO] Published message: {message}")
    #         time.sleep(5)  # Publish every 5 seconds
    # except KeyboardInterrupt:
    #     print("\n[INFO] Terminated by user.")
    # finally:
    #     client.disconnect()

if __name__ == "__main__":
    main()
