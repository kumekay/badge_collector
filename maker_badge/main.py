import gc

import asyncio

import beacon
import button
import led
import sleep
from display import init as display_init
from screens import display_badge_screen

gc.collect()
print(gc.mem_free())

LANGUAGUE = "cz"
NAME = "Robert Paulson"
COMPANY = 'Project "Mayhem"'

SLEEP_TIMEOUT = 30


# Global variables to handle the state
since_last_interaction = 0  # Time since last interaction


async def main():
    # Init peripherals
    enow = beacon.init()
    buttons = button.init()
    display = display_init()
    leds = led.init()

    print("Running...")
    asyncio.create_task(led.blink(leds, "alive"))

    asyncio.create_task(display_badge_screen(display, NAME, COMPANY, lang=LANGUAGUE, awake=True))

    tasks = [
        asyncio.create_task(sleep_handler(leds, display, buttons)),
        asyncio.create_task(beaconing(buttons[-1], leds, enow, LANGUAGUE)),
        asyncio.create_task(beacon.listener(enow, display, buttons, LANGUAGUE, leds)),
        asyncio.create_task(button_refresh(buttons)),
    ]
    await asyncio.gather(*tasks)


async def sleep_handler(leds, display, btns):
    global since_last_interaction

    while since_last_interaction < SLEEP_TIMEOUT:
        print(since_last_interaction, gc.mem_free())
        gc.collect()
        await asyncio.sleep(1)
        since_last_interaction += 1
        if since_last_interaction > SLEEP_TIMEOUT - 5:
            asyncio.create_task(led.blink(leds))

    # Go to sleep after inactivity
    await display_badge_screen(display, NAME, COMPANY, lang=LANGUAGUE, awake=False)
    sleep.sleep(btns)


async def beaconing(btn, leds, enow, lang):
    while True:
        if not btn.value:
            asyncio.create_task(led.blink(leds, "blue", 0.5, 0.125))
            beacon.send_beacon(enow, lang=lang)
        await asyncio.sleep(0.5)


async def button_refresh(btns):
    global since_last_interaction
    while True:
        for btn in btns[:-1]:
            if btn.value:
                since_last_interaction = 0
        if not btns[-1].value:
            since_last_interaction = 0
        await asyncio.sleep(0.1)


asyncio.run(main())
