import asyncio

import button
import display
import espnow
import led

BROADCAST_PEER = espnow.Peer(b"\xff" * 6)

# Global flag to send beacon
sending_beacon = False


async def main():
    # Init peripherals
    buttons = button.init()
    screen = display.init()
    leds = led.init()

    # Init espnow with broadcast
    enow = espnow.ESPNow()
    enow.peers.append(BROADCAST_PEER)

    screen_data = display.display_data()
    display.addText(screen_data, "Press the button", 1, display.COLORS["black"], 0, 20)
    screen.show(screen_data)
    screen.refresh()

    tasks = [
        asyncio.create_task(blink(leds)),
        asyncio.create_task(button_handler(buttons[0], leds)),
        asyncio.create_task(send_beacon(enow)),
        asyncio.create_task(listener(enow, screen)),
    ]
    print("Running...")
    await asyncio.gather(*tasks)


async def blink(leds):
    while True:
        print(".", end="")
        leds[-1] = led.COLORS["off"]
        leds.show()
        await asyncio.sleep(1)
        leds[-1] = led.COLORS["red"]
        leds.show()
        await asyncio.sleep(1)


async def listener(enow, screen):
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)

            screen_data = display.display_data()
            display.addText(
                screen_data, packet.msg.decode("utf-8"), 2, display.COLORS["black"], 0, 40
            )
            screen.show(screen_data)
            await asyncio.sleep(screen.time_to_refresh)
            screen.refresh()

        await asyncio.sleep(0)


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


async def send_beacon(enow):
    """Send beacon every 0.5 seconds, if button is pressed"""
    while True:
        if sending_beacon:
            enow.send(b"makers!", BROADCAST_PEER)

        await asyncio.sleep(0.5)


asyncio.run(main())
