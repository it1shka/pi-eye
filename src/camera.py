"""
Module responsible for capturing
input from camera
"""

from __future__ import annotations
from typing import AsyncIterator
import asyncio
import picamera2
from PIL import Image
import config


async def get_camera_output(
    time_startup: float, time_interval: float
) -> AsyncIterator[Image.Image]:
    """
    Async generator function that
    returns PIL image from Camera
    each {time_interval}
    """
    camera = picamera2.Picamera2()
    camera.start(show_preview=False)
    await asyncio.sleep(time_startup)
    while True:
        image = camera.capture_image()
        yield image
        await asyncio.sleep(time_interval)


async def register_camera() -> AsyncIterator[str]:
    """
    Async generator function that
    launches preconfigured Camera,
    and each {n} time it:
    1. Takes a picture
    2. Puts image into a file
    3. Yields filepath
    """
    camera_stream = get_camera_output(
        config.CameraConfig.CAMERA_STARTUP_TIME,
        config.CameraConfig.CAMERA_INTERVAL_TIME,
    )
    async for image in camera_stream:
        image_path = config.CameraConfig.CAMERA_IMAGE_PATH
        image.save(image_path)
        yield image_path
