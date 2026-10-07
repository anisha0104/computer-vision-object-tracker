import cv2

from vision.camera import Camera
from vision.detector import ObjectDetector
from vision.tracker import ObjectTracker
from vision.motion import MotionAnalyzer
from vision.fps import FPSCounter


class VideoStream:
    def __init__(self):
        self.camera = Camera()
        self.detector = ObjectDetector()
        self.tracker = ObjectTracker()
        self.motion = MotionAnalyzer()
        self.fps_counter = FPSCounter()

        self.trajectory = []

        self.latest_data = {
            "fps": 0.0,
            "detected": False,

            "center_x": 0,
            "center_y": 0,

            "direction": "STATIONARY",

            "speed": 0.0,
            "average_speed": 0.0,
            "max_speed": 0.0,
            "acceleration": 0.0,

            "distance": 0.0,
            "total_distance": 0.0,
            "displacement": 0.0,

            "tracking_duration": 0.0,
            "tracked_frames": 0,

            "trajectory": [],

            "frame_width": 640,
            "frame_height": 480
        }

    def reset_tracking(self):
        self.tracker = ObjectTracker()
        self.motion.reset()

        self.trajectory = []

        self.latest_data.update({
            "detected": False,

            "center_x": 0,
            "center_y": 0,

            "direction": "STATIONARY",

            "speed": 0.0,
            "average_speed": 0.0,
            "max_speed": 0.0,
            "acceleration": 0.0,

            "distance": 0.0,
            "total_distance": 0.0,
            "displacement": 0.0,

            "tracking_duration": 0.0,
            "tracked_frames": 0,

            "trajectory": []
        })

    def generate_frames(self):

        while True:

            frame = self.camera.read()

            if frame is None:
                break

            frame_height, frame_width = frame.shape[:2]

            self.latest_data["frame_width"] = frame_width
            self.latest_data["frame_height"] = frame_height

            fps = self.fps_counter.update()

            detection = self.detector.detect(frame)

            tracking = self.tracker.update(detection)

            motion_data = self.motion.update(detection)

            self.latest_data.update({
                "fps": round(fps, 1),
                "detected": detection is not None,
                "direction": tracking["direction"],
                "speed": round(motion_data["speed"], 1),
                "average_speed": round(
                    motion_data["average_speed"], 1
                ),
                "max_speed": round(
                    motion_data["max_speed"], 1
                ),
                "acceleration": round(
                    motion_data["acceleration"], 1
                ),
                "distance": round(
                    motion_data["distance"], 1
                ),
                "total_distance": round(
                    motion_data["total_distance"], 1
                ),
                "displacement": round(
                    motion_data["displacement"], 1
                ),
                "tracking_duration": round(
                    motion_data["tracking_duration"], 1
                ),
                "tracked_frames": motion_data[
                    "frames_tracked"
                ]
            })

            if detection:

                x = detection["x"]
                y = detection["y"]
                width = detection["width"]
                height = detection["height"]

                center_x = detection["center_x"]
                center_y = detection["center_y"]

                self.latest_data["center_x"] = center_x
                self.latest_data["center_y"] = center_y

                self.trajectory.append(
                    (center_x, center_y)
                )

                if len(self.trajectory) > 100:
                    self.trajectory.pop(0)

                self.latest_data["trajectory"] = [
                    {
                        "x": px,
                        "y": py
                    }
                    for px, py in self.trajectory
                ]

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2
                )

                cv2.circle(
                    frame,
                    (center_x, center_y),
                    5,
                    (0, 0, 255),
                    -1
                )

                for i in range(
                    1,
                    len(self.trajectory)
                ):

                    cv2.line(
                        frame,
                        self.trajectory[i - 1],
                        self.trajectory[i],
                        (255, 0, 0),
                        2
                    )

                cv2.putText(
                    frame,
                    f"X: {center_x}  Y: {center_y}",
                    (
                        x,
                        max(
                            y - 10,
                            20
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Speed: {motion_data['speed']:.1f} px/s",
                    (
                        x,
                        min(
                            y + height + 25,
                            frame_height - 10
                        )
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 255),
                    2
                )

            else:

                self.latest_data["center_x"] = 0
                self.latest_data["center_y"] = 0
                self.latest_data["direction"] = "STATIONARY"

            success, buffer = cv2.imencode(
                ".jpg",
                frame
            )

            if not success:
                continue

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + buffer.tobytes()
                + b"\r\n"
            )