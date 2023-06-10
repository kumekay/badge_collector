import asyncio
import time

import adafruit_ssd1680
import board
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import wrap_text_to_lines
from adafruit_display_text.label import Label

BLACK = 0x000000
WHITE = 0xFFFFFF
COLORS = {"black": BLACK, "white": WHITE}

# Define ePaper display resolution
DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 122


def addText(display_data, text, scale, color, x_cord, y_cord):
    group = displayio.Group(scale=scale, x=x_cord, y=y_cord)
    text_label = Label(terminalio.FONT, text=text, color=color)
    group.append(text_label)
    display_data.append(group)


def init():
    # Define board pinout
    board_spi = board.SPI()  # Uses SCK and MOSI
    board_epd_cs = board.D41
    board_epd_dc = board.D40
    board_epd_reset = board.D39
    board_epd_busy = board.D42

    # Prepare ePaper display
    displayio.release_displays()
    display_bus = displayio.FourWire(
        board_spi,
        command=board_epd_dc,
        chip_select=board_epd_cs,
        reset=board_epd_reset,
        baudrate=1000000,
    )
    time.sleep(1)
    display = adafruit_ssd1680.SSD1680(
        display_bus,
        width=DISPLAY_WIDTH,
        height=DISPLAY_HEIGHT,
        rotation=270,
        busy_pin=board_epd_busy,
        seconds_per_frame=5,
    )

    return display


def centered_text(display_data, text, x, y, width, height, scale=1, wrap=0):
    text_group = displayio.Group(scale=scale)

    if wrap > 0:
        text = "\n".join(wrap_text_to_lines(text, wrap))

    text_area = Label(terminalio.FONT, text=text, color=BLACK)
    text_width = text_area.bounding_box[2]
    text_group.x = x + width // 2 - text_width * text_group.scale // 2
    text_group.y = y + height // 2
    text_group.append(text_area)
    display_data.append(text_group)


def rect_with_text(display_data, text, x, y, width, height, scale=1, with_rect=False):
    """Draws a rectangle with centered text"""

    if with_rect:
        rect = Rect(
            x,
            y,
            width - 1,  # -1 to make space between adjacent rectangles
            height,
            fill=WHITE,
            outline=BLACK,
        )
        display_data.append(rect)

    # # Creating centered text
    text_group = displayio.Group(scale=scale)
    text_area = Label(terminalio.FONT, text=text, color=BLACK)
    text_width = text_area.bounding_box[2]
    text_group.x = x + width // 2 - text_width * text_group.scale // 2
    text_group.y = y + height // 2
    text_group.append(text_area)
    display_data.append(text_group)


def draw_key(display_data, known_letters, lang, key_len=0):
    """Draws a key with known letters"""
    key_width = 12
    key_height = 20

    key_text = "Klic:" if lang.lower() == "cz" else "Key:"

    # Key label
    text_group = displayio.Group(scale=1, x=0, y=10)
    key_label = Label(terminalio.FONT, text=key_text, color=BLACK)
    text_group.append(key_label)
    display_data.append(text_group)
    key_label_width = key_label.bounding_box[2]

    # Draw chars
    for i in range(key_len):
        rect_with_text(
            display_data,
            known_letters.get(str(i), "_").upper(),
            i * key_width + key_label_width + 2,
            0,
            key_width,
            key_height,
        )


def draw_question(display_data, question, answers):
    """Draws a question and its answers"""
    answer_width = 50
    answer_height = 25

    # Draw question
    centered_text(
        display_data,
        question,
        0,
        0,
        DISPLAY_WIDTH,
        DISPLAY_HEIGHT - answer_height,
        scale=2,
        wrap=20,
    )

    # Draw answers
    for i, answer in enumerate(answers):
        rect_with_text(
            display_data,
            answer,
            i * answer_width,
            DISPLAY_HEIGHT - answer_height,
            answer_width,
            answer_height,
            with_rect=True,
        )


def draw_badge(display_data, name, company, awake, lang):
    centered_text(
        display_data,
        name,
        0,
        20,
        DISPLAY_WIDTH,
        2 * (DISPLAY_HEIGHT // 3) - 30,
        scale=3,
    )
    centered_text(
        display_data,
        company,
        0,
        2 * (DISPLAY_HEIGHT // 3) - 40,
        DISPLAY_WIDTH,
        DISPLAY_HEIGHT - 30,
        scale=2,
    )

    if lang.lower() == "cz":
        awake_text = 'Stisknete "boot" pro ' + ("vyhledavany otazky" if awake else "probuzeni")
    else:
        awake_text = 'Press "boot" to ' + ("look for a question" if awake else "awake")

    centered_text(
        display_data,
        awake_text,
        0,
        DISPLAY_HEIGHT - 12,
        DISPLAY_WIDTH,
        12,
    )


def build_display_data():
    data = displayio.Group()
    display_background = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    display_color_palette = displayio.Palette(1)
    display_color_palette[0] = COLORS["white"]

    # Append tilegrid with the background to the display data
    data.append(displayio.TileGrid(display_background, pixel_shader=display_color_palette))

    return data


async def show(display, display_data):
    await asyncio.sleep(display.time_to_refresh)

    while display.busy:
        await asyncio.sleep(0.2)

    display.show(display_data)
    display.refresh()
