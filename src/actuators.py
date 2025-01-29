"""
This module is responsible
for physical response to the intruder
using RPi GPIO lines and external
actuators
"""

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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._warning_led, GPIO.OUT)
        GPIO.setup(self._ok_led, GPIO.OUT)

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
