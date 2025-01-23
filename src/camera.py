"""
Module responsible for capturing
input from camera
"""

from __future__ import annotations
from typing import AsyncIterator
import asyncio
import picamera2
from PIL import Image

CAMERA_STARTUP_TIME = 2


async def get_camera_output(time_interval: float) -> AsyncIterator[Image.Image]:
    """
    Function that returns camera view image
    each {time_interval}
    """
    camera = picamera2.Picamera2()
    camera.start_preview()
    await asyncio.sleep(CAMERA_STARTUP_TIME)
    while True:
        image = camera.capture_image()
        yield image
        await asyncio.sleep(time_interval)
