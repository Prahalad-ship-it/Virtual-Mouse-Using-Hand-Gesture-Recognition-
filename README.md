Virtual Mouse Using Hand Gesture Recognition
Control your computer mouse using just your hand and a webcam — no physical mouse needed. This project uses MediaPipe for real-time hand tracking and PyAutoGUI to control your system cursor through gestures.

Features

Move cursor with your index finger
Left click by pinching index finger + thumb
Right click by pinching middle finger + thumb
Double click by pinching index + middle fingers together
Drag by holding index finger up alone
Scroll up with 3 fingers raised
Scroll down with 4 fingers raised
Live gesture label displayed on the webcam feed
On-screen controls legend shown at all times


Requirements

Python 3.8+
Webcam
Windows / macOS / Linux


Installation
1. Clone the repository
bashgit clone https://github.com/Prahalad-ship-it/Virtual-Mouse-Using-Hand-Gesture-Recognition-.git
cd Virtual-Mouse-Using-Hand-Gesture-Recognition-
2. Install dependencies
bashpip install opencv-python mediapipe pyautogui
3. Download the MediaPipe Hand Landmarker model
The script will automatically download the model on first run. Make sure you have an internet connection.
Or download it manually:

https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
Place it in the same folder as main.py


Running the Program
bashpython main.py
A window called "Virtual Mouse" will open showing your webcam feed with hand landmarks drawn on it.
Press Q to quit.

Gesture Controls
GestureActionMove index fingerMove cursorIndex + Thumb pinchLeft clickMiddle + Thumb pinchRight clickIndex + Middle pinchDouble clickIndex finger only upDrag (hold)3 fingers upScroll up4 fingers upScroll downQ keyQuit program

Tips for Best Performance

Lighting: Use good front-facing light. Avoid bright windows behind you
Distance: Keep your hand 1-2 feet from the camera
Background: A plain background helps detection accuracy
Speed: Move your hand slowly and deliberately at first
Hand position: Keep fingers spread so MediaPipe can detect them clearly


Troubleshooting
AttributeError: module 'mediapipe' has no attribute 'solutions'
This version of MediaPipe (0.10+) removed the old API. The code in this repo uses the new Tasks API — make sure you are using main.py from this repo.
ModuleNotFoundError
Run the install command again:
bashpip install opencv-python mediapipe pyautogui
Webcam window does not appear
Check your taskbar — the window may be minimized or behind other windows.
Cursor moves but clicks do not work
Pinch more firmly and hold the pinch for a moment. You can also increase the pinch threshold in main.py:
pythonPINCH_THRESHOLD = 0.05  # increase to 0.07 or 0.08 if needed
Warning messages in terminal (XNNPACK, inference_feedback_manager)
These are harmless — the program still works fine. They are internal MediaPipe logs.

Project Structure
Virtual-Mouse-Using-Hand-Gesture-Recognition-/
├── main.py                  # Main script
├── hand_landmarker.task     # MediaPipe model (auto-downloaded)
└── README.md                # This file

How It Works
Webcam -> OpenCV frame -> MediaPipe Hand Landmarker
                                    |
                         21 hand landmarks detected
                                    |
                    Fingertip positions mapped to screen
                                    |
                       PyAutoGUI moves/clicks mouse
MediaPipe detects 21 landmarks on your hand. The key ones used:

Landmark 4  — Thumb tip
Landmark 8  — Index fingertip (cursor control)
Landmark 12 — Middle fingertip
Landmark 16 — Ring fingertip
Landmark 20 — Pinky fingertip


Built With

OpenCV — Webcam capture and display
MediaPipe — Hand landmark detection
PyAutoGUI — Mouse and keyboard control


Author
Srinaga Prahalad Pillutla
Enjoy

License
This project is open source and available under the MIT License.