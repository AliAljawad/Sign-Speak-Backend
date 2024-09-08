from fastapi import FastAPI
import pickle
import mediapipe as mp
import numpy as np
import cv2


app=FastAPI()
# Load pre-trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize Mediapipe components
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Labels dictionary (A-Z)
labels_dict = {chr(i): chr(i) for i in range(ord('A'), ord('Z') + 1)}

def process_frame(frame: np.ndarray) -> str:
    """Process a single frame to predict the hand sign."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    results = hands.process(frame_rgb)  # Process with Mediapipe
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []
            x_, y_ = [], []

            # Extract landmarks
            for lm in hand_landmarks.landmark:
                x, y = lm.x, lm.y
                x_.append(x)
                y_.append(y)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

            # Ensure the correct number of landmarks is present
            if len(data_aux) == 42:  
                prediction = model.predict([np.asarray(data_aux)])
                return labels_dict.get(prediction[0], "Unknown")

    return "No hand detected"
