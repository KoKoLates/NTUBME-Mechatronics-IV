import cv2

class VideoCamera(object):
    def __init__(self) -> None:
        # using the OpenCV to capture the video stream from device 0.
        # check the webcam device file first before use it.
        self.video = cv2.VideoCapture(0)

    def __del__(self) -> None:
        self.video.release()

    def get_frame(self) -> bytes:
        ret, frame = self.video.read()
        # using Motion JPEG, but OpenV defaults to capture raw images
        # it's needed to encode into JPEG for video stream displaying.
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()