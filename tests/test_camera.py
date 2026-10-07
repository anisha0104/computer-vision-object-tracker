from unittest.mock import MagicMock

from vision.camera import Camera


def test_camera_initializes():
    camera = Camera(
        camera_index=9999
    )

    assert camera is not None

    camera.release()


def test_camera_read_returns_none_when_unavailable():
    camera = Camera(
        camera_index=9999
    )

    result = camera.read()

    assert result is None

    camera.release()


def test_camera_release():
    camera = Camera(
        camera_index=9999
    )

    camera.release()

    assert camera.camera is not None