import board
import neopixel

COLORS = {
    "off": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
}


def init(led_pin=board.D18, led_count=4, led_brightness=0.1, led_auto_write=False):
    led_matrix = neopixel.NeoPixel(
        led_pin, led_count, brightness=led_brightness, auto_write=led_auto_write
    )

    return led_matrix
