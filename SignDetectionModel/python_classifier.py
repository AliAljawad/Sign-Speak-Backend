import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the trained model from a pickle file
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']  # Extract the model from the dictionary

# Initialize webcam capture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe hands module and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Set up the hands object with static image mode and minimum detection confidence
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Dictionary to map model predictions to corresponding sign language characters
labels_dict = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I',
               'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R',
               'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'}

# Start real-time video capture loop
while True:

    data_aux = []  # Store normalized hand landmarks for prediction
    x_ = []  # Store x-coordinates of hand landmarks
    y_ = []  # Store y-coordinates of hand landmarks

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Get the frame's height and width
    H, W, _ = frame.shape

    # Convert the frame from BGR to RGB (required for MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hand landmarks
    results = hands.process(frame_rgb)

    # If hand landmarks are detected, process them
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks and connections on the frame
            mp_drawing.draw_landmarks(
                frame,  # image to draw on
                hand_landmarks,  # detected hand landmarks
                mp_hands.HAND_CONNECTIONS,  # hand connections to draw
                mp_drawing_styles.get_default_hand_landmarks_style(),  # style for landmarks
                mp_drawing_styles.get_default_hand_connections_style()  # style for connections
            )

            # Extract x and y coordinates of the landmarks
            x_ = []
            y_ = []
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            # Normalize the landmarks by subtracting the minimum x and y values
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))  # Normalize x-coordinate
                data_aux.append(y - min(y_))  # Normalize y-coordinate

            # Predict the sign language character if the required number of landmarks is available
            if len(data_aux) == 42:  # Ensures 21 points (x, y) * 2 = 42
                prediction = model.predict([np.asarray(data_aux)])  # Make prediction using the model
                predicted_character = labels_dict[prediction[0]]  # Map prediction to character
                print(predicted_character)  # Print predicted character

                # Draw bounding box around the detected hand and display predicted character
                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)  # Draw black rectangle
                cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                            cv2.LINE_AA)  # Display the predicted character on the frame

    # Show the frame with hand landmarks and prediction
    cv2.imshow('frame', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
