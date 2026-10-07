import cv2
import numpy as np


class ObjectDetector:
    def __init__(self):
        self.lower_color = np.array(
            [20, 100, 100]
        )

        self.upper_color = np.array(
            [35, 255, 255]
        )

        self.minimum_area = 500

    def detect(self, frame):
        if frame is None:
            return None

        if frame.size == 0:
            return None

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        mask = cv2.inRange(
            hsv,
            self.lower_color,
            self.upper_color
        )

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        largest_contour = max(
            contours,
            key=cv2.contourArea
        )

        area = cv2.contourArea(
            largest_contour
        )

        if area < self.minimum_area:
            return None

        x, y, width, height = cv2.boundingRect(
            largest_contour
        )

        center_x = x + width // 2
        center_y = y + height // 2

        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "center_x": center_x,
            "center_y": center_y,
            "area": area
        }