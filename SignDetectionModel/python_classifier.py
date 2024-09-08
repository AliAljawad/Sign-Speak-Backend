import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Set up hand detection model
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)


