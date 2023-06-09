import board
import touchio
from digitalio import DigitalInOut, Direction, Pull

BUTTON_PINS = [board.D5, board.D4, board.D3, board.D2, board.D1]
BOOT_PIN = board.D0


def init(touch_threshold=20000):
    btns = []
    for pin in BUTTON_PINS:
        button = touchio.TouchIn(pin)
        button.threshold = touch_threshold
        btns.append(button)

    btn = DigitalInOut(BOOT_PIN)
    btn.direction = Direction.INPUT
    btn.pull = Pull.UP
    btns.append(btn)

    return btns


def deinit(btns):
    for button in btns:
        button.deinit()
