"""
Module responsible for
face recognition
"""

from __future__ import annotations
from enum import Enum
import face_recognition


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

    def check_image(self, image_path: str) -> RecognitionResult:
        """
        Function that
        1. Loads given image
        2. Scraps encodings from that image
        3. Compares those encodings to known faces
        4. Outputs its verdict
        """
        ...
