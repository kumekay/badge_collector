import time

import adafruit_ssd1680
import board
import displayio
import terminalio
from adafruit_display_text import label

COLORS = {"black": 0x000000, "white": 0xFFFFFF}

# Define ePaper display resolution
DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 122


# Function for append text to the display data
def addText(display_data, text, scale, color, x_cord, y_cord):
    group = displayio.Group(scale=scale, x=x_cord, y=y_cord)
    text_label = label.Label(terminalio.FONT, text=text, color=color)
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
    )

    return display


def display_data():
    data = displayio.Group()
    display_background = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    display_color_palette = displayio.Palette(1)
    display_color_palette[0] = COLORS["white"]

    # Append tilegrid with the background to the display data
    data.append(
        displayio.TileGrid(display_background, pixel_shader=display_color_palette)
    )

    return data
