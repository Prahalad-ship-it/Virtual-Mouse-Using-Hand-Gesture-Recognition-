import cv2
import pyautogui
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
import os
import math

pyautogui.FAILSAFE = False

model_path = "hand_landmarker.task"
screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

PINCH_THRESHOLD = 0.05
left_clicking = False
right_clicking = False
dragging = False

def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def fingers_up(lm):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    return [lm[tips[i]].y < lm[pips[i]].y for i in range(4)]

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

        gesture_text = ""

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                index_tip  = hand_landmarks[8]
                thumb_tip  = hand_landmarks[4]
                middle_tip = hand_landmarks[12]
                ring_tip   = hand_landmarks[16]
                pinky_tip  = hand_landmarks[20]

                # Move mouse
                x = int(index_tip.x * screen_w)
                y = int(index_tip.y * screen_h)
                pyautogui.moveTo(x, y)

                up = fingers_up(hand_landmarks)
                # up[0]=index, up[1]=middle, up[2]=ring, up[3]=pinky

                pinch_im = dist(index_tip, thumb_tip)   # index+thumb
                pinch_mm = dist(middle_tip, thumb_tip)  # middle+thumb

                # ✅ LEFT CLICK — pinch index + thumb
                if pinch_im < PINCH_THRESHOLD:
                    if not left_clicking:
                        pyautogui.click()
                        left_clicking = True
                        gesture_text = "LEFT CLICK"
                else:
                    left_clicking = False

                # ✅ RIGHT CLICK — pinch middle + thumb
                if pinch_mm < PINCH_THRESHOLD:
                    if not right_clicking:
                        pyautogui.rightClick()
                        right_clicking = True
                        gesture_text = "RIGHT CLICK"
                else:
                    right_clicking = False

                # ✅ DOUBLE CLICK — index + middle both up, pinch together
                if dist(index_tip, middle_tip) < PINCH_THRESHOLD:
                    pyautogui.doubleClick()
                    gesture_text = "DOUBLE CLICK"

                # ✅ DRAG — index up only (hold)
                if up[0] and not up[1] and not up[2] and not up[3]:
                    if not dragging:
                        pyautogui.mouseDown()
                        dragging = True
                        gesture_text = "DRAG"
                else:
                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

                # ✅ SCROLL UP — index + middle + ring up
                if up[0] and up[1] and up[2] and not up[3]:
                    pyautogui.scroll(3)
                    gesture_text = "SCROLL UP"

                # ✅ SCROLL DOWN — all fingers up (open hand)
                if up[0] and up[1] and up[2] and up[3]:
                    pyautogui.scroll(-3)
                    gesture_text = "SCROLL DOWN"

                # Draw landmarks
                for landmark in hand_landmarks:
                    cx = int(landmark.x * frame.shape[1])
                    cy = int(landmark.y * frame.shape[0])
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # HUD display
        if gesture_text:
            cv2.putText(frame, gesture_text, (50, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # Controls legend
        cv2.putText(frame, "Index+Thumb = Left Click",    (10, frame.shape[0]-130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "Middle+Thumb = Right Click",  (10, frame.shape[0]-110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "Index+Middle pinch = Dbl Clk",(10, frame.shape[0]-90),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "Index only = Drag",           (10, frame.shape[0]-70),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "3 fingers up = Scroll Up",    (10, frame.shape[0]-50),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "4 fingers up = Scroll Down",  (10, frame.shape[0]-30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, "Q = Quit",                    (10, frame.shape[0]-10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255),   1)

        cv2.imshow('Virtual Mouse', frame)
        cv2.setWindowProperty('Virtual Mouse', cv2.WND_PROP_TOPMOST, 1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()