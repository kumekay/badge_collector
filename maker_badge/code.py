import asyncio

import button
import display
import led


async def main():
    # Init peripherals
    buttons = button.init()
    screen = display.init()
    leds = led.init()

    screen_data = display.display_data()
    display.addText(screen_data, "Test", 3, display.COLORS["black"], 70, 20)
    screen.show(screen_data)
    screen.refresh()

    led_task = asyncio.create_task(blink(leds))
    btn_task = asyncio.create_task(set_color(buttons, leds))

    print("Running...")
    await asyncio.gather(led_task, btn_task)


async def blink(leds):
    while True:
        print(".", end="")
        leds[-1] = led.COLORS["off"]
        leds.show()
        await asyncio.sleep(1)
        leds[-1] = led.COLORS["red"]
        leds.show()
        await asyncio.sleep(1)


async def set_color(btns, leds):
    colors = [
        led.COLORS["red"],
        led.COLORS["green"],
        led.COLORS["blue"],
        led.COLORS["white"],
        led.COLORS["off"],
    ]

    while True:
        for i in range(5):
            if btns[i].value:
                leds[0] = colors[i]
                leds.show()

        await asyncio.sleep(0.05)


asyncio.run(main())
