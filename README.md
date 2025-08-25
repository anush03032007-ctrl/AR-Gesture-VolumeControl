# AR-Gesture-VolumeControl
AR Gesture Volume Control is a real-time computer vision project that lets you control system volume with just your hand gestures — no keyboard or mouse needed.

Built using Python, OpenCV, and Google’s MediaPipe, the system tracks the thumb and index finger landmarks from your webcam. By measuring the distance between them, it dynamically adjusts your device’s audio volume.

The project demonstrates how Augmented Reality + Hand Tracking can be combined for intuitive Human-Computer Interaction (HCI). It’s lightweight, runs fully on-device (no cloud processing), and shows how vision + simple math can unlock powerful AR experiences.
#######################################################################################################################################################################
🔹 **Features**

👋 Real-time hand tracking with MediaPipe (21 landmark detection).

🔊 Volume control by adjusting the distance between thumb and index finger.

🎨 Visual feedback: fingertip markers, connection line, and color-coded volume levels.

⚡ High FPS performance (20+ FPS on standard laptop webcams).

🔐 Privacy-first: all processing happens locally, no data is sent online.
#######################################################################################################################################################################
🛠 **Tech Stack**

 1) Python 3.10+

 2) OpenCV – for video processing & visualization

 3) MediaPipe – hand detection & landmark tracking

 4) PyCaw – system audio control (Windows)

 5) NumPy – distance calculations & interpolation
