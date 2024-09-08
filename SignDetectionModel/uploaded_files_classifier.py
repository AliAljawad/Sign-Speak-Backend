from fastapi import FastAPI,File, UploadFile
import pickle
import mediapipe as mp
import numpy as np
import cv2
from io import BytesIO
import os
import time


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

@app.post("/predict_image")
async def predict_image(file: UploadFile = File(...)):
    """Predict the sign language character from an uploaded image."""
    image = np.frombuffer(await file.read(), np.uint8)  # Read the file as bytes
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Decode to OpenCV format
    prediction = process_frame(image)  # Predict the character
    return {"Translation": prediction}

@app.post("/predict_video")
async def predict_video(file: UploadFile = File(...)):
    """Predict the sign language characters from an uploaded video."""
    temp_file = BytesIO(await file.read())
    temp_file.seek(0)

    with open('temp_video.mp4', 'wb') as f:
        f.write(temp_file.read())

    video_capture = cv2.VideoCapture('temp_video.mp4')
    if not video_capture.isOpened():
        return {"message": "Error opening video file"}

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    interval = int(fps)

    predictions = []
    frame_count = 0

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % interval == 0:
            prediction = process_frame(frame)
            predictions.append(prediction)

        # Match the frame rate of video
        time.sleep(1 / fps)

    video_capture.release()
    os.remove('temp_video.mp4')

    return {"Translation": predictions}
