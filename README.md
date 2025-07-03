# 🎨 Scribbly - AI-Powered Air Sketching App

**Scribbly** is an innovative air-drawing web application that allows users to sketch on a virtual canvas using real-time hand gestures captured through a webcam. Built with **OpenCV**, **MediaPipe**, **Flask**, and **React**, it enables a touch-free, creative drawing experience with gesture recognition and intuitive brush controls.


## 🚀 Features

-  **Draw with Hand Gestures**: Use finger movements detected by your webcam to draw.
-  **Select Colors and Brush Sizes**: Choose from multiple colors and adjust brush thickness.
-  **Draw Shapes with Gestures**: Create rectangles, circles, and lines using intuitive hand signs.
-  **Save Artwork**: Instantly download your sketch as a PNG image.
-  **Clear Canvas**: One-click clear option to reset your canvas.
-  **Canvas Preview**: Live preview of your drawing on a separate canvas.
-  **Responsive UI**: Clean, full-screen interface optimized for desktops.
-  **Session Management**: Automatically resets the webcam and canvas between sessions.

## 🛠️ Tech Stack

###  Frontend
- React.js - Frontend library used to build a dynamic, component-based user interface with real-time canvas preview.
- HTML5 -  Enables drawing functionality and live rendering on the frontend.
- CSS3 - For custom styling, responsive layout, and beautiful animations.
- React Router - A powerful routing library for React that enables seamless navigation between pages without full page reloads, creating a smooth single-page application experience.

###  Backend
- Flask - Lightweight Python web framework used to handle video streaming, gesture processing, and API routes.
- Flask-CORS - A Flask extension that enables Cross-Origin Resource Sharing (CORS), allowing your React frontend to securely communicate with the Flask backend on different ports
- OpenCV - Computer vision library used to capture webcam input and render drawing operations frame-by-frame.
- MediaPipe - Google's ML solution for real-time hand gesture tracking and landmark detection from camera feed.
- NumPy - Fundamental scientific computing library in Python, used here for efficient image and matrix operations

##
