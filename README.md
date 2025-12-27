# Hand-Gesture-Game-Controller
# Project Overview
The Hand Gesture Game Controller is an AI-based computer vision project that allows users to control games using real-time hand gestures instead of a physical keyboard.It demonstrates the practical use of AI, Computer Vision, and Human–Computer Interaction concepts.
# Features

Real-time hand gesture recognition

Touchless game control

AI-based hand landmark detection

Gesture-to-keyboard mapping

Smooth left, right, jump, and duck actions
# How It Works

OpenCV captures the live video feed from the webcam.

MediaPipe Hands detects and tracks hand landmarks in real time.

Hand gestures are analyzed based on finger positions and hand movement.

Detected gestures are mapped to keyboard keys using the pynput library.

These virtual key presses control the game (Left, Right, Jump, Duck).

# Gestures Used

Move Left: Hand moves to the left side of the screen

Move Right: Hand moves to the right side of the screen

Jump: Closed fist gesture

Duck: Thumb + pinky finger gesture
# Technologies & Libraries Used

Python

OpenCV

MediaPipe

pynput

Time module
# System Requirements

Laptop/Desktop with a webcam

Python 3.8 or above

CPU-based system (GPU not required)

Good lighting for accurate hand detection
# Installation
pip install opencv-python mediapipe pynput

# Run the Project
python hand_gesture.py
⭐ If you like this project, feel free to star the repository!
