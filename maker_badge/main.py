import asyncio

import beacon
import button
import led
import sleep
from display import init as display_init
from screens import display_badge_screen

LANGUAGUE = "cz"
NAME = "Robert Paulson"
COMPANY = 'Project "Mayhem"'

SLEEP_TIMEOUT = 15


# Global variables to handle the state
sending_beacon = False
since_last_interaction = 0  # Time since last interaction


async def main():
    # Init peripherals
    beacon.init()
    button.init()
    display = display_init()
    leds = led.init()

    print("Running...")
    asyncio.create_task(led.blink(leds, "alive"))

    asyncio.create_task(display_badge_screen(display, NAME, COMPANY, lang=LANGUAGUE, awake=True))

    tasks = [
        asyncio.create_task(sleep_handler(leds, display)),
    ]
    await asyncio.gather(*tasks)


async def sleep_handler(leds, display):
    global since_last_interaction

    while since_last_interaction < SLEEP_TIMEOUT:
        print(since_last_interaction)
        await asyncio.sleep(1)
        since_last_interaction += 1
        if since_last_interaction > SLEEP_TIMEOUT - 5:
            asyncio.create_task(led.blink(leds))

    # Go to sleep after inactivity
    await display_badge_screen(display, NAME, COMPANY, lang=LANGUAGUE, awake=False)
    sleep.sleep()


async def button_handler(btn, leds):
    global sending_beacon
    while True:
        if btn.value:
            leds[0] = led.COLORS["green"]
            leds.show()
            sending_beacon = True
        else:
            leds[0] = led.COLORS["off"]
            leds.show()
            sending_beacon = False

        await asyncio.sleep(0.05)


asyncio.run(main())
