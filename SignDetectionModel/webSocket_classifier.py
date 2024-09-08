import asyncio
import websockets
import cv2
import mediapipe as mp
import numpy as np
import pickle

# Load the model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
labels_dict = {chr(i): chr(i) for i in range(ord('A'), ord('Z') + 1)}

# Set up the WebSocket server
async def handle_connection(websocket, path):
    while True:
        # Receive the camera feed from the client
        frame = await websocket.recv()
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Process the frame using the model
        data_aux = []
        x_ = []
        y_ = []

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x_ = []
                y_ = []

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

                if len(data_aux) == 42:  # Adjust if needed
                    prediction = model.predict([np.asarray(data_aux)])
                    predicted_character = labels_dict[prediction[0]]

                    # Send the predicted character back to the client
                    await websocket.send(predicted_character)

# Start the WebSocket server
if __name__ == "__main__":
    print("WebSocket server started on 0.0.0.0:8002")
    start_server = websockets.serve(handle_connection, "0.0.0.0", 8002)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
