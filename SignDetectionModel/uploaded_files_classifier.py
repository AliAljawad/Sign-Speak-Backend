from fastapi import FastAPI
import pickle
import mediapipe as mp
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
