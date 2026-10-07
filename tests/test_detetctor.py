import cv2
import numpy as np

from vision.detector import ObjectDetector


def test_detector_initializes():
    detector = ObjectDetector()

    assert detector is not None
    assert detector.minimum_area == 500


def test_detector_returns_none_when_no_object():
    detector = ObjectDetector()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    result = detector.detect(frame)

    assert result is None


def test_detector_returns_none_for_invalid_frame():
    detector = ObjectDetector()

    assert detector.detect(None) is None


def test_detector_returns_none_for_empty_frame():
    detector = ObjectDetector()

    frame = np.empty(
        (0, 0, 3),
        dtype=np.uint8
    )

    result = detector.detect(frame)

    assert result is None


def test_detector_ignores_small_object():
    detector = ObjectDetector()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    cv2.circle(
        frame,
        (320, 240),
        5,
        (0, 255, 255),
        -1
    )

    result = detector.detect(frame)

    assert result is None


def test_detector_finds_yellow_object():
    detector = ObjectDetector()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    cv2.circle(
        frame,
        (320, 240),
        50,
        (0, 255, 255),
        -1
    )

    result = detector.detect(frame)

    assert result is not None

    assert "center_x" in result
    assert "center_y" in result
    assert "width" in result
    assert "height" in result
    assert "area" in result


def test_detector_detects_object_near_corner():
    detector = ObjectDetector()

    frame = np.zeros(
        (480, 640, 3),
        dtype=np.uint8
    )

    cv2.circle(
        frame,
        (50, 50),
        40,
        (0, 255, 255),
        -1
    )

    result = detector.detect(frame)

    assert result is not None
    assert result["center_x"] > 0
    assert result["center_y"] > 0