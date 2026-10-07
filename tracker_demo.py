import cv2

from vision.camera import Camera
from vision.detector import ObjectDetector
from vision.tracker import ObjectTracker
from vision.motion import MotionAnalyzer
from vision.fps import FPSCounter


camera = Camera()
detector = ObjectDetector()
tracker = ObjectTracker()
motion = MotionAnalyzer()
fps_counter = FPSCounter()

trajectory = []

while True:

    frame = camera.read()

    if frame is None:
        print("Unable to read from camera.")
        break

    fps = fps_counter.update()

    detection = detector.detect(frame)

    tracking = tracker.update(
        detection
    )

    motion_data = motion.update(
        detection
    )

    if detection:

        x = detection["x"]
        y = detection["y"]

        width = detection["width"]
        height = detection["height"]

        center_x = detection["center_x"]
        center_y = detection["center_y"]

        trajectory.append(
            (center_x, center_y)
        )

        if len(trajectory) > 100:
            trajectory.pop(0)

        # Bounding box
        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            2
        )

        # Center point
        cv2.circle(
            frame,
            (center_x, center_y),
            5,
            (0, 0, 255),
            -1
        )

        # Draw trajectory
        for i in range(
            1,
            len(trajectory)
        ):
            cv2.line(
                frame,
                trajectory[i - 1],
                trajectory[i],
                (255, 0, 0),
                2
            )

        # Coordinates
        cv2.putText(
            frame,
            f"X: {center_x}  Y: {center_y}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

    # FPS
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Tracking statistics
    cv2.putText(
        frame,
        f"Tracked Frames: {motion_data['frames_tracked']}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
    frame,
    f"Direction: {tracking['direction']}",
    (20, 150),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (0, 255, 255),
    2
    )


    cv2.putText(
    frame,
    f"Speed: {motion_data['speed']:.1f} px/s",
    (20, 180),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (255, 255, 255),
    2
)

    cv2.putText(
        frame,
        f"Distance: {motion_data['total_distance']:.1f}px",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"Displacement: {motion_data['displacement']:.1f}px",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Computer Vision Object Tracker",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()