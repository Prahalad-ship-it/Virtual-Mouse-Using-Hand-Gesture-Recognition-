import cv2
import mediapipe as mp
import pyautogui

from mediapipe.python.solutions import hands as mp_hands_module
from mediapipe.python.solutions import drawing_utils as mp_drawing

hands = mp_hands_module.Hands(max_num_hands=1, min_detection_confidence=0.7)

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark[8]
            x = int(lm.x * screen_w)
            y = int(lm.y * screen_h)

            pyautogui.moveTo(x, y)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands_module.HAND_CONNECTIONS)

    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()