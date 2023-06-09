import asyncio

import board
import neopixel

COLORS = {
    "off": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "alive": (50, 50, 50),
}


def init(led_pin=board.D18, led_count=4, led_brightness=0.1, led_auto_write=False):
    led_matrix = neopixel.NeoPixel(
        led_pin, led_count, brightness=led_brightness, auto_write=led_auto_write
    )

    return led_matrix


async def blink(
    leds,
    color="red",
    duration=3,
    interval=0.5,
):
    """Blink the LEDs in the given color for the given duration"""

    while duration > 0:
        leds.fill(COLORS[color.lower()])
        leds.show()
        await asyncio.sleep(interval)
        leds.fill(COLORS["off"])
        leds.show()
        await asyncio.sleep(interval)
        duration -= interval * 2
