import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(camera_index)

    def is_opened(self):
        return self.camera.isOpened()

    def read(self):
        if not self.is_opened():
            return None

        success, frame = self.camera.read()

        if not success:
            return None

        return frame

    def release(self):
        if self.camera is not None:
            self.camera.release()