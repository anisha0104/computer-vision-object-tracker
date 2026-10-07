# 👁️ Computer Vision Object Tracker

A real-time computer vision system built with **Python and OpenCV** that detects and tracks a colored object using a camera feed, analyzes its movement, and displays live telemetry through a professional web dashboard.

The system combines **object detection, object tracking, motion analysis, trajectory visualization, FPS monitoring, and a Flask-based dashboard** into one engineering-focused application.

---

## 🚀 Project Overview

The Computer Vision Object Tracker processes live camera frames and identifies a target object based on its color.

Once detected, the system calculates:

- 📍 Object center coordinates
- 📦 Bounding box
- ↔️ Direction of movement
- 🏃 Instantaneous speed
- 📈 Average speed
- ⚡ Acceleration
- 📏 Distance travelled
- 📐 Displacement
- 🏁 Maximum speed
- ⏱️ Tracking duration
- 🎞️ Processing FPS
- 🧭 Object trajectory

The processed information is displayed through a **Flask web dashboard** in real time.

---

## ✨ Features

### 🎯 Object Detection

- Detects a target object using HSV color segmentation.
- Identifies the largest matching contour.
- Filters out objects below a minimum area.
- Calculates the object's bounding box.
- Determines the center coordinates of the detected object.

### 🧭 Object Tracking

- Tracks the object's position between consecutive frames.
- Calculates movement in the X and Y directions.
- Determines movement direction:
  - `UP`
  - `DOWN`
  - `LEFT`
  - `RIGHT`
  - `UP-RIGHT`
  - `UP-LEFT`
  - `DOWN-RIGHT`
  - `DOWN-LEFT`
  - `STATIONARY`

### 📊 Motion Analysis

The system continuously calculates:

- Instantaneous speed
- Average speed
- Maximum speed
- Acceleration
- Distance travelled
- Total distance
- Displacement
- Tracking duration
- Number of tracked frames

> Speed and distance are represented in image-space pixels because the system does not currently perform physical camera calibration.

### 📈 Trajectory Visualization

The object's previous positions are stored and connected to create a live movement trajectory.

This allows the user to visually analyze the object's path across the camera frame.

### 🎞️ FPS Monitoring

A dedicated FPS counter measures the approximate processing rate of the vision pipeline.

### 🌐 Web Dashboard

The project includes a Flask-based dashboard providing:

- Live camera feed
- Real-time telemetry
- Performance metrics
- Object coordinates
- Movement direction
- Tracking trajectory
- Processing status
- Tracking session reset

### 🔄 Tracking Reset

The dashboard includes a **Reset Session** function that clears:

- Previous object position
- Motion calculations
- Distance
- Displacement
- Speed statistics
- Acceleration
- Tracking duration
- Trajectory history
- Frame tracking count

---

# 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │ Camera / Webcam │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    OpenCV       │
                    │ Frame Capture   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Object Detector │
                    │ HSV Segmentation│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Object Tracker  │
                    │ Position Change │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Motion Analyzer │
                    │ Speed / Distance│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ FPS Monitoring  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Flask Web App   │
                    └────────┬────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │   Web Dashboard       │
                 │                       │
                 │ Camera + Telemetry    │
                 │ Coordinates           │
                 │ Motion Statistics     │
                 │ Trajectory            │
                 └───────────────────────┘
````

---

# 🧠 Computer Vision Pipeline

The detection pipeline follows these stages:

```text
Camera Frame
     ↓
BGR Image
     ↓
HSV Conversion
     ↓
Color Thresholding
     ↓
Binary Mask
     ↓
Contour Detection
     ↓
Largest Valid Contour
     ↓
Bounding Rectangle
     ↓
Object Center
     ↓
Tracking
     ↓
Motion Analysis
     ↓
Visualization
```

---

# 🎨 Object Detection

The detector uses **HSV color space** instead of directly operating on BGR values.

HSV makes it easier to isolate objects based on their:

* Hue
* Saturation
* Brightness

The current implementation is configured to detect a **yellow-colored object**.

The detector:

1. Converts the frame from BGR to HSV.
2. Applies a lower and upper HSV threshold.
3. Creates a binary mask.
4. Finds external contours.
5. Selects the largest contour.
6. Rejects objects smaller than the minimum area.
7. Calculates the bounding rectangle.
8. Calculates the object's center.

---

# 📐 Object Position

For a detected bounding box:

```text
(x, y)
   ┌───────────────┐
   │               │
   │       ●       │
   │     Center    │
   │               │
   └───────────────┘
          width
```

The center is calculated using:

```text
center_x = x + width / 2
center_y = y + height / 2
```

These coordinates are then passed to the tracking and motion-analysis systems.

---

# 🧭 Movement Tracking

The tracker compares the current object position with the previous position.

```text
Previous Position
        ●
         \
          \
           \
            ●
        Current Position
```

The movement is calculated using:

```text
dx = current_x - previous_x

dy = current_y - previous_y
```

The direction is then determined from the sign and magnitude of `dx` and `dy`.

A small movement threshold is used to prevent insignificant frame-to-frame movement from being interpreted as meaningful movement.

---

# 🏃 Motion Analysis

The system calculates movement using image-space coordinates.

### Distance Between Frames

The Euclidean distance is:

```text
distance = √(dx² + dy²)
```

### Total Distance

The total distance is accumulated over all tracked frames:

```text
total_distance = Σ distance
```

### Displacement

Displacement represents the direct distance between the starting position and current position:

```text
displacement = √(dx² + dy²)
```

where `dx` and `dy` represent the difference between the starting and current coordinates.

### Speed

Speed is calculated from:

```text
speed = distance / time
```

The resulting unit is:

```text
pixels / second
```

### Average Speed

Average speed is calculated using:

```text
average_speed =
total_distance / tracking_duration
```

### Acceleration

Acceleration is estimated from the change in speed over time:

```text
acceleration =
(current_speed - previous_speed) / elapsed_time
```

---

# ⚠️ Important Measurement Note

The current system operates in **image coordinates**.

Therefore:

```text
Distance → pixels
Speed → pixels/second
Acceleration → pixels/second²
```

These values should not be interpreted as physical metres, metres/second, or metres/second² without camera calibration.

A future version can convert image-space measurements into real-world measurements using:

* Camera calibration
* Known reference dimensions
* Perspective correction
* Homography
* Camera-to-world coordinate mapping

---

# 📊 Dashboard

The web dashboard provides several sections.

### Live Camera

Displays the processed camera stream with:

* Bounding box
* Object center
* Coordinates
* Speed
* Movement trajectory

### Primary Telemetry

Displays the most important live tracking information.

### Performance Telemetry

Includes:

* Average speed
* Maximum speed
* Acceleration
* Tracking duration
* Tracked frames
* Frame resolution

### Coordinates

Displays the current X and Y position of the detected object.

### Processing Pipeline

Provides a visual representation of the computer-vision workflow.

### Trajectory

Displays the historical movement path of the detected object.

### System Status

Displays the current state of the tracking system.

---

# 🌐 Flask API

The application exposes several HTTP endpoints.

## Home

```text
GET /
```

Loads the main dashboard.

---

## Video Feed

```text
GET /video_feed
```

Provides the processed camera stream using an MJPEG response.

---

## System Status

```text
GET /api/status
```

Returns the application status.

Example:

```json
{
    "project": "Computer Vision Object Tracker",
    "status": "running"
}
```

---

## Live Metrics

```text
GET /api/metrics
```

Returns the latest tracking and motion telemetry.

Example structure:

```json
{
    "fps": 30.0,
    "detected": true,
    "center_x": 320,
    "center_y": 240,
    "direction": "RIGHT",
    "speed": 125.4,
    "average_speed": 98.2,
    "max_speed": 180.6,
    "acceleration": 25.3,
    "distance": 4.2,
    "total_distance": 1520.7,
    "displacement": 380.4,
    "tracking_duration": 15.4,
    "tracked_frames": 460
}
```

---

## Reset Tracking

```text
POST /api/reset
```

Resets the current tracking session.

Example response:

```json
{
    "status": "reset",
    "message": "Tracking session reset successfully"
}
```

---

# 📁 Project Structure

```text
computer-vision-object-tracker/
│
├── vision/
│   ├── __init__.py
│   ├── camera.py
│   ├── detector.py
│   ├── tracker.py
│   ├── motion.py
│   ├── fps.py
│   └── stream.py
│
├── tests/
│   ├── __init__.py
│   ├── test_camera.py
│   ├── test_detector.py
│   ├── test_tracker.py
│   └── test_motion.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧩 Module Description

| Module        | Responsibility                                           |
| ------------- | -------------------------------------------------------- |
| `camera.py`   | Camera initialization and frame capture                  |
| `detector.py` | Color-based object detection                             |
| `tracker.py`  | Position tracking and direction detection                |
| `motion.py`   | Speed, distance, displacement and acceleration           |
| `fps.py`      | FPS calculation                                          |
| `stream.py`   | Integrates camera, detection, tracking and visualization |
| `app.py`      | Flask web application and API                            |
| `index.html`  | Dashboard structure                                      |
| `style.css`   | Dashboard styling                                        |
| `script.js`   | Live telemetry and dashboard interaction                 |
| `tests/`      | Automated unit tests                                     |

---

# 🛠️ Tech Stack

### Programming

* Python 3
* HTML5
* CSS3
* JavaScript

### Computer Vision

* OpenCV
* NumPy

### Backend

* Flask

### Testing

* Pytest

### Development Tools

* Visual Studio Code
* Git
* GitHub
* PowerShell

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/anisha0104/computer-vision-object-tracker.git
```

Navigate into the project:

```bash
cd computer-vision-object-tracker
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

# 🧪 Run Tests

Run the complete automated test suite:

```bash
python -m pytest
```

The tests cover:

* Camera initialization
* Camera failure handling
* Object detection
* Invalid frames
* Small-object filtering
* Yellow-object detection
* Object tracking
* Direction detection
* Distance calculation
* Motion analysis
* Speed calculation
* Maximum speed
* Average speed
* Tracking duration
* Reset functionality

---

# ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally on:

```text
http://127.0.0.1:5000
```

Open the address in a browser.

Make sure a compatible webcam/camera is available to the system.

---

# 🎥 Using the Tracker

1. Start the Flask application.
2. Open the dashboard in a browser.
3. Allow the application to access the camera if required.
4. Place a yellow object within the camera frame.
5. Move the object around.
6. Observe the bounding box and center point.
7. Monitor the live telemetry.
8. Observe the movement trajectory.
9. Use **Reset Session** to start a new tracking session.

---

# 🧪 Testing Strategy

The project follows a modular testing approach.

Each major component is tested independently.

```text
Camera
   ↓
Camera Tests

Detector
   ↓
Detection Tests

Tracker
   ↓
Tracking Tests

Motion Analyzer
   ↓
Motion Tests

Flask Application
   ↓
API / Integration Tests
```

This structure makes individual components easier to debug, maintain, and extend.

---

# 🔐 Error Handling

The system includes handling for several failure conditions:

* Camera unavailable
* Camera frame unavailable
* Empty frames
* Invalid frames
* No detected object
* Objects below minimum detection area
* Failed frame encoding
* Unknown API endpoints
* Internal server errors

When an object is not detected, the system returns safe telemetry values rather than crashing.

---

# 🎯 Engineering Applications

Although this project uses a simple color-based detection method, the architecture can be extended to more advanced computer-vision applications.

Potential applications include:

### 🏭 Industrial Monitoring

* Object position monitoring
* Conveyor tracking
* Manufacturing inspection
* Equipment monitoring

### 🤖 Robotics

* Robot vision
* Object following
* Navigation
* Position estimation
* Motion analysis

### 🏎️ Motorsport

The project can be extended toward motorsport data analysis through:

* Vehicle tracking
* Wheel movement analysis
* Track object detection
* Camera-based telemetry
* Racing-line analysis
* Speed estimation
* Motion trajectory analysis

### 🚀 Research & Education

* Projectile tracking
* Motion experiments
* Computer-vision demonstrations
* Robotics experiments
* Physics measurements

---

# 🔮 Future Improvements

The current system provides a strong foundation for more advanced computer-vision functionality.

Planned improvements include:

### 🎯 Advanced Object Detection

Replace simple color segmentation with:

* YOLO
* MobileNet
* TensorFlow
* PyTorch
* Deep-learning object detectors

### 📏 Real-World Measurement

Implement camera calibration and perspective transformation to convert:

```text
pixels → metres
```

This would enable physically meaningful:

```text
distance
speed
acceleration
```

measurements.

### 🎥 Video File Support

Add support for:

* MP4
* AVI
* MOV

files in addition to live camera input.

### 📊 Historical Telemetry

Store tracking sessions and allow users to compare:

* Maximum speed
* Average speed
* Distance
* Acceleration
* Tracking duration

### 📈 Advanced Analytics

Add:

* Speed graphs
* Acceleration graphs
* Position graphs
* Velocity vectors
* Movement heatmaps

### 🧠 Machine Learning

Replace HSV-based detection with trained machine-learning models for more robust object recognition.

### 🌐 Remote Deployment

A future architecture could support browser-based camera streaming or uploaded video processing so that the system can operate without requiring a physical camera connected to the server.

---

# 📌 Current Limitations

* Detection currently relies on a predefined yellow HSV color range.
* Only the largest matching contour is tracked.
* Measurements are in image-space pixels.
* No camera calibration is currently implemented.
* Camera input currently assumes a locally accessible camera.
* Lighting changes can affect color-based detection.
* Occlusion may cause tracking to temporarily fail.
* The current tracker does not use advanced predictive tracking algorithms.

---

# 📚 Learning Outcomes

This project provided practical experience with:

* Computer vision fundamentals
* OpenCV
* HSV color segmentation
* Contour detection
* Bounding boxes
* Coordinate systems
* Object tracking
* Motion mathematics
* Real-time data processing
* FPS measurement
* Flask
* REST-style APIs
* HTML/CSS/JavaScript dashboards
* Automated testing with Pytest
* Modular Python architecture
* Git and GitHub
* Debugging real-time applications

---

# 🏆 Project Highlights

### Real-Time Computer Vision

Processes camera frames continuously and detects the target object.

### Modular Architecture

Detection, tracking, motion analysis, camera handling, and FPS monitoring are separated into independent modules.

### Engineering Telemetry

Transforms raw object positions into meaningful movement metrics.

### Web-Based Visualization

Provides a professional dashboard for monitoring the system.

### Automated Testing

Core computer-vision and motion components are covered by unit tests.

### Extensible Design

The architecture can be extended toward machine learning, robotics, industrial monitoring, and motorsport applications.

---

# 👩‍💻 Author

**Anisha**

Electronics & Telecommunication Engineering

Interested in:

* Electronics
* Embedded Systems
* Software Engineering
* Computer Vision
* Robotics
* Data Analysis
* Motorsport Technology
* Formula 1 Engineering

---

# 📜 License

This project is intended for educational, portfolio, and engineering demonstration purposes.

---

⭐ If you find this project interesting, feel free to explore the repository and its implementation.

````

### Then do this 👇

Save **`README.md`**, then run:

```powershell
git add README.md
git commit -m "Add professional project documentation"
git push origin main
````

After that, **Project 3 is basically portfolio-ready** 🔥🏎️.
