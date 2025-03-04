import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
import geocoder
from geopy.distance import geodesic
import folium
import osmnx as ox
import networkx as nx
import pandas as pd
import time
import pygame
import sounddevice as sd
import requests
import speech_recognition as sr
import threading

# Global Variables
embedding_file = "face_embeddings.npy"
face_embeddings = np.load(embedding_file, allow_pickle=True).item() if os.path.exists(embedding_file) else {}
current_location = None
speed = 0
sos_triggered = False

# Initialize Face Recognition
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

# CCTV Face Recognition
def face_recognition():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)
        
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                x, y, w_box, h_box = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                face_roi = frame[y:y+h_box, x:x+w_box]
                
                try:
                    face_embedding = DeepFace.represent(face_roi, model_name='Facenet')[0]['embedding']
                    identified = identify_face(face_embedding)
                    color = (0, 0, 255) if "ALERT" in identified else (0, 255, 0)
                    cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
                    cv2.putText(frame, identified, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                except:
                    pass

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def identify_face(face_embedding):
    threshold = 10  # Lower value = more strict
    best_match = "SAFE"
    best_distance = float("inf")
    
    for stored_name, stored_embeddings in face_embeddings.items():
        for stored_embedding in stored_embeddings:
            distance = np.linalg.norm(np.array(face_embedding) - np.array(stored_embedding))
            if distance < threshold and distance < best_distance:
                best_match = f"ALERT: {stored_name} detected!"
                best_distance = distance
    return best_match

# GPS Speed Tracker
def gps_speed_tracker():
    global current_location, speed
    prev_location, prev_time = None, None
    while True:
        g = geocoder.ip("me")
        if g.latlng:
            lat, lon = g.latlng
            curr_time = time.time()
            current_location = (lat, lon)
            
            if prev_location and prev_time:
                distance = geodesic(prev_location, current_location).meters
                time_diff = curr_time - prev_time
                speed = distance / time_diff if time_diff > 0 else 0  # m/s
            
            prev_location, prev_time = current_location, curr_time
        time.sleep(5)

# Safe Route Mapping
def create_safe_route():
    crime_hotspots = pd.DataFrame({'latitude': [28.6500, 28.6350], 'longitude': [77.2000, 77.2150]})
    G = ox.graph_from_place("Delhi, India", network_type='walk')
    if current_location:
        orig_node = ox.distance.nearest_nodes(G, X=current_location[1], Y=current_location[0])
        dest_node = ox.distance.nearest_nodes(G, X=77.2900, Y=28.6100)  # Example destination
        safe_route = nx.shortest_path(G, orig_node, dest_node, weight='length')
        return safe_route
    return None

# SOS Emergency
def send_sos_alert():
    global sos_triggered
    location_api = "https://ipinfo.io/loc"
    location = requests.get(location_api).text.strip()
    print(f"EMERGENCY! Location: {location}")
    sos_triggered = False

def listen_for_sos():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Listening for SOS trigger...")
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "help" in command:
                    send_sos_alert()
            except:
                pass

# Running Modules in Parallel
threads = [
    threading.Thread(target=face_recognition),
    threading.Thread(target=gps_speed_tracker),
    threading.Thread(target=listen_for_sos)
]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
