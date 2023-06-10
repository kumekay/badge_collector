import gc

import asyncio

import beacon
import button
import led
import sleep
from display import init as display_init
from screens import display_badge_screen, load_letters
from state import g

gc.collect()

LANGUAGUE = "cz"
NAME = "Robert Paulson"
COMPANY = 'Project "Mayhem"'

SLEEP_TIMEOUT = 30


# Global variables to handle the state
since_last_interaction = 0  # Time since last interaction


async def main():
    # Init peripherals
    g.enow = beacon.init()
    g.buttons = button.init()
    g.display = display_init()
    g.leds = led.init()
    load_letters()
    g.lang = LANGUAGUE
    g.name = NAME
    g.company = COMPANY

    asyncio.create_task(led.blink("alive"))

    asyncio.create_task(display_badge_screen(NAME, COMPANY, lang=LANGUAGUE, awake=True))

    tasks = [
        asyncio.create_task(sleep_handler()),
        asyncio.create_task(beaconing(g.buttons[-1], LANGUAGUE)),
        asyncio.create_task(beacon.listener(LANGUAGUE)),
        asyncio.create_task(button_refresh()),
    ]
    await asyncio.gather(*tasks)


async def sleep_handler():
    global since_last_interaction

    while since_last_interaction < SLEEP_TIMEOUT:
        print(since_last_interaction, gc.mem_free())
        gc.collect()
        await asyncio.sleep(1)
        since_last_interaction += 1
        if since_last_interaction > SLEEP_TIMEOUT - 5:
            asyncio.create_task(led.blink())

    # Go to sleep after inactivity
    await sleep.sleep()


async def beaconing(btn, lang):
    while True:
        if not btn.value:
            asyncio.create_task(led.blink("blue", 0.5, 0.125))
            beacon.send_beacon(lang=lang)
        await asyncio.sleep(0.5)


async def button_refresh():
    global since_last_interaction
    while True:
        for btn in g.buttons[:-1]:
            if btn.value:
                since_last_interaction = 0
        if not g.buttons[-1].value:
            since_last_interaction = 0
        await asyncio.sleep(0.1)


asyncio.run(main())
