"""
Raspberry Pi application to track
activity in your room
"""

import asyncio
import camera
import mail_service
import faces
from faces import RecognitionResult
import actuators


async def main() -> None:
    """
    For each generated image,
    launches face recongition,
    and if face is unknown,
    sends emails
    """

    image_stream = camera.register_camera()
    detector = faces.FaceRecognition()
    actuators_service = actuators.ActuatorService()
    with mail_service.MailServer() as mail_server:
        async for image_path in image_stream:
            verdict = detector.check_image(image_path)
            match verdict:
                case RecognitionResult.NO_FACES:
                    print("Everything is clear")
                case RecognitionResult.KNOWN_FACES:
                    print("Detected known faces")
                    asyncio.create_task(actuators_service.flash_pin("ok"))
                case RecognitionResult.UNKNOWN_FACES:
                    print("Intruders detected. Sending mails...")
                    mail_server.dispatch_emails(image_path)
                    asyncio.create_task(actuators_service.flash_pin("warning"))
                case _:
                    print("Failed to analyse the image")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
