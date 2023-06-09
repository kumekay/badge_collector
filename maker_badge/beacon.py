import asyncio

import espnow

BROADCAST_PEER = espnow.Peer(b"\xff" * 6)


def init():
    # Init espnow with broadcast
    enow = espnow.ESPNow()
    enow.peers.append(BROADCAST_PEER)
    return enow


def send_beacon(enow, lang="cz"):
    enow.send(b"!" + lang.encode("utf-8"), BROADCAST_PEER)


async def listener(enow, screen):
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)

            # TODO: process incoming question

            print("Screen busy, time to refresh: ", screen.time_to_refresh)

        await asyncio.sleep(0)
