import board
import touchio

BUTTON_PINS = [board.D5, board.D4, board.D3, board.D2, board.D1]


def init(touch_threshold=20000):
    btns = []
    for pin in BUTTON_PINS:
        button = touchio.TouchIn(pin)
        button.threshold = touch_threshold
        btns.append(button)

    return btns


def deinit(btns):
    for button in btns:
        button.deinit()
