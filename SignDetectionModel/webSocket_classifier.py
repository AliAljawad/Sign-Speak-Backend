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
        frame = await websocket.recv()
        frame = np.frombuffer(frame, dtype=np.uint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

# Start the WebSocket server
if __name__ == "__main__":
    print("WebSocket server started on 0.0.0.0:8002")
    start_server = websockets.serve(handle_connection, "0.0.0.0", 8002)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()