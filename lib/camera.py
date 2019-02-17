from contextlib import contextmanager

import cv2


class Camera:
    video_capture = None

    @classmethod
    @contextmanager
    def open_camera(cls):
        cls.video_capture = cv2.VideoCapture(0)

        yield

        cls.video_capture.release()
        cv2.destroyAllWindows()

    @classmethod
    def get_frame(cls):
        _, frame = cls.video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        return small_frame[:, :, ::-1]
