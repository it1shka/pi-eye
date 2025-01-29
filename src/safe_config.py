"""
Module that handles constants
for application configuration
"""


class CameraConfig:
    """
    Class holding configuration of camera
    """

    CAMERA_IMAGE_PATH = "./camera/camera_image.jpg"
    CAMERA_STARTUP_TIME = 2
    CAMERA_INTERVAL_TIME = 5


class EmailConfig:
    """
    Class holding configuration of email service
    """

    SERVICE_MAIL = "PUT YOUR MAIL HERE"
    SERVICE_PASSWORD = "PUT YOUR PASSWORD HERE"
    SMTP_SERVER = "PUT YOUR SMTP SERVER HERE"
    SMTP_SERVER_PORT = -1  # PUT YOUR PORT HERE
    SUBJECT = "PI EYE - ILLEGAL FACE DETECTED"
    CONTENT = "Face not allowed in database detected.\nTimestamp: %s"
    USER_EMAILS = []  # PUT YOUR EMAILS HERE


class RecognitionConfig:
    """
    Class holding configuration of Face Recognition
    """

    FACES_PATH = "./faces"
