"""
Module responsible for
face recognition
"""

from __future__ import annotations
from enum import Enum
import os
import face_recognition
import config


class RecognitionResult(Enum):
    """
    Represents result of face recognition
    1. No faces: image doesn't contain any people
    2. Known faces: all faces from the image are in the base
    3. Unknown faces: at least one face on the image is unknown
    """

    NO_FACES = 0
    KNOWN_FACES = 1
    UNKNOWN_FACES = 2


class FaceRecognition:
    """
    Class responsible for face recognition.
    On init loads encodings of known faces,
    then exposes them to the function
    check_image
    """

    def __init__(self) -> None:
        """Loads known encodings"""
        faces_path = config.RecognitionConfig.FACES_PATH
        images_path_list = [
            os.path.join(faces_path, file_path) for file_path in os.listdir(faces_path)
        ]
        all_encodings = []
        for image_path in images_path_list:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            all_encodings = [*all_encodings, *encodings]
        self._encodings = all_encodings

    def check_image(self, image_path: str) -> RecognitionResult:
        """
        Function that
        1. Loads given image
        2. Scraps encodings from that image
        3. Compares those encodings to known faces
        4. Outputs its verdict
        """
        image = face_recognition.load_image_file(image_path)
        current_encodings = face_recognition.face_encodings(image)
        if len(current_encodings) <= 0:
            return RecognitionResult.NO_FACES
        for face_encoding in current_encodings:
            results = face_recognition.compare_faces(self._encodings, face_encoding)
            if not any(results):
                return RecognitionResult.UNKNOWN_FACES
        return RecognitionResult.KNOWN_FACES
