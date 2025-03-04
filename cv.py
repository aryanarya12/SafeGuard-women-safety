import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
import os

rapist_image_path = r"C:\Users\DEVENDER\Desktop\crime mappong\datset\rapist.jpg"

if not os.path.exists(rapist_image_path):
    print(f"Error: Image file '{rapist_image_path}' not found!")
    exit()

embedding_file = "rapist_embedding.npy"

if os.path.exists(embedding_file):
    rapist_embedding = np.load(embedding_file)
    print("✅ Rapist embedding loaded successfully!")
else:
    try:
        img = cv2.imread(rapist_image_path)
        if img is None:
            raise ValueError("Error: Unable to load image. Check file path or format!")

        rapist_embedding = DeepFace.represent(img, model_name='Facenet')[0]['embedding']
        np.save(embedding_file, rapist_embedding)  # Save embedding
        print("✅ Rapist embedding created and saved!")
    except Exception as e:
        print("❌ Error extracting embedding:", str(e))
        exit()
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

def identify_face(face_embedding):
    distance = np.linalg.norm(np.array(face_embedding) - np.array(rapist_embedding))
    return "Threat Detected" if distance < 10 else "Safe"

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("✅ Webcam opened successfully! Press 'q' to quit.")

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

            # Attempt to extract DeepFace embedding
            try:
                face_embedding = DeepFace.represent(face_roi, model_name='Facenet')[0]['embedding']
                status = identify_face(face_embedding)
            except:
                status = "Unknown"

            
            color = (0, 0, 255) if status == "Threat Detected" else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
            cv2.putText(frame, status, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

# ✅ Step 7: Cleanup
cap.release()
cv2.destroyAllWindows()
print("✅ Program exited successfully!")
