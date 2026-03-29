import cv2
import pyautogui
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
import urllib.request
import os

# Download the hand landmarker model if not present
model_path = "hand_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        model_path
    )
    print("Downloaded!")

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

options = HandLandmarkerOptions(
    base_options=python.BaseOptions(model_asset_path=model_path),
    running_mode=RunningMode.IMAGE,
    num_hands=1
)

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = landmarker.detect(mp_image)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                # Index fingertip = landmark 8
                lm = hand_landmarks[8]
                x = int(lm.x * screen_w)
                y = int(lm.y * screen_h)
                pyautogui.moveTo(x, y)

                # Draw dots on hand
                for landmark in hand_landmarks:
                    cx = int(landmark.x * frame.shape[1])
                    cy = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        cv2.imshow('Virtual Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()