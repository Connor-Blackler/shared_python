import cv2
from deepface import DeepFace


class ImageRecognition:
    def __init__(self, image_path: str) -> None:
        self._image_path = image_path

    def process(self) -> dict:
        img = cv2.imread(self._image_path)
        return DeepFace.analyze(img)
