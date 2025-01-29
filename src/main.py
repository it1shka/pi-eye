"""
Raspberry Pi application to track
activity in your room
"""

import asyncio
import camera
import mail_service
import face_recognition


async def main() -> None:
    """
    For each generated image,
    launches face recongition,
    and if face is unknown,
    sends emails
    """

    with mail_service.MailServer() as mail_server:
        image_stream = camera.register_camera()
        async for image_path in image_stream:
            invalid = face_recognition.detect_invalid_face(image_path)
            if invalid:
                mail_server.dispatch_emails(image_path)
                print('Intruder found. Sending emails...')
            else:
                print('Everything is alright')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
