import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model
from efficientnet.tfkeras import preprocess_input

# Load the trained model
model_path = 'best_model.h5'
loaded_model = load_model(model_path)

# Set the input size
input_size = 128  # Adjust as needed

def preprocess_image(img):
    img = cv2.resize(img, (input_size, input_size))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img

def predict_face(image):
    img = preprocess_image(image)
    prediction = loaded_model.predict(img)
    class_label = "Real" if prediction > 0.8 else "Fake"
    confidence = prediction[0, 0] if class_label == "Fake" else 1 - prediction[0, 0]
    return class_label, confidence

def process_video(video_path, output_path='output.avi'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    detector = MTCNN()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Changed to mp4v codec
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    fake_frame_count = 0
    total_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        total_frames += 1
        frame_is_fake = False

        # Detect faces
        faces = detector.detect_faces(frame)

        # Loop through each detected face
        for face in faces:
            bounding_box = face['box']
            confidence = face['confidence']

            if confidence > 0.95:  # Adjust confidence threshold if needed
                x, y, w, h = bounding_box
                face_image = frame[y:y+h, x:x+w]

                # Predict using the trained model
                class_label, confidence = predict_face(face_image)

                # Set color based on prediction
                color = (0, 0, 255) if class_label == "Fake" else (0, 255, 0)
                
                if class_label == "Fake":
                    frame_is_fake = True

                # Display result on the frame
                label = f"{class_label} ({confidence:.2%})"
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

        if frame_is_fake:
            fake_frame_count += 1
            
            cv2.imshow('Frame Analysis', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Write the frame to the output video
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Make final decision
    is_fake = fake_frame_count >= 10
    result = {
        'is_fake': is_fake,
        'fake_frames': fake_frame_count,
        'total_frames': total_frames,
        'classification': 'FAKE' if is_fake else 'REAL'
    }
    
    return result
