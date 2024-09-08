import os
import pickle
import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Directory containing the dataset of images
DATA_DIR = './data'
data = []   # List to store the processed hand landmark data
labels = [] # List to store the corresponding labels for each image

# Loop through each subdirectory in the data folder
for dir_ in os.listdir(DATA_DIR):
    dir_path = os.path.join(DATA_DIR, dir_)
    if os.path.isdir(dir_path):  # Check if it's a directory
        # Loop through each image in the subdirectory
        for img_path in os.listdir(dir_path):
            img = cv2.imread(os.path.join(dir_path, img_path))  # Read the image
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert image to RGB format

            # Process the image to detect hand landmarks
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:  # If hand landmarks are detected
                for hand_landmarks in results.multi_hand_landmarks:
                    data_aux = []  # Temporary list to store normalized landmark data

                    x_ = []  # List to store x-coordinates of landmarks
                    y_ = []  # List to store y-coordinates of landmarks

                    # Extract x and y coordinates of each hand landmark
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y

                        x_.append(x)
                        y_.append(y)

                    # Normalize the landmarks by subtracting the minimum x and y values
                    min_x = min(x_)
                    min_y = min(y_)

                    # Store the normalized coordinates
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        data_aux.append(x - min_x)
                        data_aux.append(y - min_y)

                    # Append the processed landmark data and corresponding label to the lists
                    data.append(data_aux)
                    labels.append(dir_)

# Save the processed data and labels into a pickle file
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)
