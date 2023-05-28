import board
import touchio


def init(touch_threshold=20000):
    btn_pins = [board.D5, board.D4, board.D3, board.D2, board.D1]
    btns = []
    for pin in btn_pins:
        btns.append(touchio.TouchIn(pin))
        btns[-1].threshold = touch_threshold

    return btns
