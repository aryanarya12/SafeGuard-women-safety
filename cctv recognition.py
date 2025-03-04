import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
import os

# Directory to store face embeddings
embedding_file = "face_embeddings.npy"

# Load stored embeddings or initialize a new dictionary
if os.path.exists(embedding_file):
    face_embeddings = np.load(embedding_file, allow_pickle=True).item()
else:
    face_embeddings = {}

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.7)

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("\n✅ Press 'S' to capture and register a new face.")
print("✅ Press 'Q' to exit.")

mode = input("\nChoose mode (1- Register Face, 2- Recognize Face): ").strip()

if mode == "1":  # Register Face Mode
    name = input("\nEnter your name: ").strip()

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

                cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), (255, 0, 0), 2)
                cv2.putText(frame, "Press 'S' to Save", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv2.imshow('Face Registration', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Save face image
            try:
                face_embedding = DeepFace.represent(face_roi, model_name='Facenet')[0]['embedding']
                
                # Append multiple embeddings instead of overwriting
                if name in face_embeddings:
                    face_embeddings[name].append(face_embedding)
                else:
                    face_embeddings[name] = [face_embedding]

                np.save(embedding_file, face_embeddings)
                print(f"✅ Face data for {name} saved successfully! ({len(face_embeddings[name])} samples)")
                
            except:
                print("⚠ Face not detected properly. Try again.")

        if key == ord('q'):  # Quit
            break

    print("✅ Registration complete!")
    cap.release()
    cv2.destroyAllWindows()

elif mode == "2":  # Recognize Face Mode
    def identify_face(face_embedding):
        """Compare detected face embedding with stored embeddings"""
        threshold = 10  # Lower = more strict, higher = more lenient

        best_match = "✅ SAFE"
        best_distance = float("inf")

        for stored_name, stored_embeddings in face_embeddings.items():
            for stored_embedding in stored_embeddings:
                distance = np.linalg.norm(np.array(face_embedding) - np.array(stored_embedding))
                if distance < threshold and distance < best_distance:
                    best_match = f"⚠ ALERT: {stored_name} detected!"
                    best_distance = distance

        return best_match

    print("\n✅ Recognizing faces... Press 'Q' to quit.")

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
                    status = identify_face(face_embedding)
                except:
                    status = "Unknown"

                color = (0, 0, 255) if "ALERT" in status else (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w_box, y + h_box), color, 2)
                cv2.putText(frame, status, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Live Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Program exited successfully!")

else:
    print("❌ Invalid choice! Exiting.")
    cap.release()
    cv2.destroyAllWindows()