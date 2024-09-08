from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from io import BytesIO
import numpy as np
import cv2
import mediapipe as mp
import pickle
from typing import List
import os
import time

app = FastAPI()

# Load the pre-trained machine learning model and other necessary components
model_dict = pickle.load(open('./model.p', 'rb'))  # Load the pickled model from file
model = model_dict['model']  # Extract the actual model

# Initialize MediaPipe hands solution for hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # Utility to draw the hands' landmarks
mp_drawing_styles = mp.solutions.drawing_styles  # Pre-defined drawing styles for hands landmarks
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)  # Initialize the hand detector

# Dictionary to map model predictions (A-Z) to their respective characters
labels_dict = {chr(i): chr(i) for i in range(ord('A'), ord('Z') + 1)}

def process_frame(frame: np.ndarray) -> str:
    """Process a single frame to predict the hand sign."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame from BGR (OpenCV) to RGB (MediaPipe)
    results = hands.process(frame_rgb)  # Process the frame using MediaPipe hand detection
    
    if results.multi_hand_landmarks:  # Check if any hands were detected
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []  # Placeholder for the processed hand landmarks data
            x_, y_ = [], []  # Lists to store the normalized x and y coordinates of the landmarks

            # Extract x and y coordinates of each hand landmark
            for lm in hand_landmarks.landmark:
                x, y = lm.x, lm.y
                x_.append(x)
                y_.append(y)

            # Normalize coordinates by subtracting the minimum values
            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

            # Check if the landmark data has the expected length for the model
            if len(data_aux) == 42:  # Adjust the number of landmarks as needed
                prediction = model.predict([np.asarray(data_aux)])  # Make a prediction using the model
                return labels_dict.get(prediction[0], "Unknown")  # Return the predicted sign character

    return "No hand detected"  # Return this if no hands are detected

@app.post("/predict_image")
async def predict_image(file: UploadFile = File(...)):
    """Predict the sign language character from an uploaded image."""
    image = np.frombuffer(await file.read(), np.uint8)  # Read the uploaded image file and convert to NumPy array
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # Decode the image to a format suitable for OpenCV
    prediction = process_frame(image)  # Process the frame and get the prediction
    return {"Translation": prediction}  # Return the predicted character as a response

@app.post("/predict_video")
async def predict_video(file: UploadFile = File(...)):
    """Predict the sign language characters from an uploaded video."""
    # Read the uploaded video file into a temporary in-memory file
    temp_file = BytesIO(await file.read())
    temp_file.seek(0)  # Reset the file pointer to the beginning

    # Write the video to a temporary file on disk
    with open('temp_video.mp4', 'wb') as f:
        f.write(temp_file.read())

    # Open the video file using OpenCV
    video_capture = cv2.VideoCapture('temp_video.mp4')
    if not video_capture.isOpened():  # Check if the video file was opened successfully
        return {"message": "Error opening video file"}

    # Get the frames per second (FPS) of the video to determine processing interval
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    interval = int(fps)  # Process every second of the video based on FPS

    predictions = []  # List to store the predictions for each processed frame
    frame_count = 0  # Counter to keep track of frames
    while True:
        ret, frame = video_capture.read()  # Read the next frame from the video
        if not ret:  # Break the loop if no more frames are available
            break
        frame_count += 1  # Increment the frame counter
        if frame_count % interval == 0:  # Process one frame per second
            prediction = process_frame(frame)  # Process the current frame and get prediction
            predictions.append(prediction)  # Append the prediction to the list
        time.sleep(1 / fps)  # Sleep to synchronize with the video frame rate

    # Release the video capture object and delete the temporary video file
    video_capture.release()
    os.remove('temp_video.mp4')

    return {"Translation": predictions}  # Return the list of predictions
