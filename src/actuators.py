"""
This module is responsible
for physical response to the intruder
using RPi GPIO lines and external
actuators
"""

from __future__ import annotations
from typing import Literal
import RPi.GPIO as GPIO
import asyncio
import config


ActuatorPin = Literal["warning"] | Literal["ok"]


class ActuatorService:
    """Class that controls actuators"""

    def __init__(self) -> None:
        """Initializes GPIO"""
        self._warning_led = config.GPIOConfig.WARNING_LED
        self._ok_led = config.GPIOConfig.OK_LED
        self._flash_time = config.GPIOConfig.FLASH_TIME
        self._buzzer = config.GPIOConfig.BUZZER
        GPIO.setmode(GPIO.BCM)
        for output_pin in [self._warning_led, self._ok_led, self._buzzer]:
            GPIO.setup(output_pin, GPIO.OUT)

    async def flash_pin(self, pin: ActuatorPin) -> None:
        """
        Flashing specified LED
        for fixed number of seconds
        """
        current_pin: int
        match pin:
            case "warning":
                current_pin = self._warning_led
            case "ok":
                current_pin = self._ok_led
        GPIO.output(current_pin, GPIO.HIGH)
        await asyncio.sleep(self._flash_time)
        GPIO.output(current_pin, GPIO.LOW)

    async def make_noise(self) -> None:
        """
        Makes negative noise using passive buzzer
        Duration is the same as for LEDs
        """
        GPIO.output(self._buzzer, GPIO.HIGH)
        await asyncio.sleep(self._flash_time)
        GPIO.output(self._buzzer, GPIO.LOW)

    def cleanup(self) -> None:
        """Cleans up GPIO"""
        GPIO.cleanup()

    def __enter__(self) -> ActuatorService:
        """Acquiring from `with`"""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exiting `with`"""
        self.cleanup()
