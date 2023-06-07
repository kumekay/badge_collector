import asyncio
import json

import espnow

# BROADCAST_PEER = espnow.Peer(b"\xff" * 6)

# Dictionary of known peers
# Keys are MAC addresses, values - number of packets sent
known_peers = {}

# Question to be sent
# Format: (question, (answers), correct_answer_index, secret_char, secret_char_position)
QUESTION = (
    "The first ESP chip is ...",
    (
        "ESP32",
        "ESP8266",
        "ESP32-C3",
        "ESP32-S2",
    ),
    1,
    "E",
    2,
)
QUESTION_BYTES = json.dumps(QUESTION).encode("utf-8")


async def listener(enow):
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)

            # If we don't know this peer, add it to the dictionary
            if packet.msg == b"makers!" and packet.mac not in known_peers:
                print("New peer found:", packet.mac)
                enow.peers.append(espnow.Peer(packet.mac))
                known_peers[packet.mac] = 0

        await asyncio.sleep(0)


async def sender(enow):
    while True:
        # Send question to all known peers 5 times, then remove them from the list
        for peer in enow.peers:
            if known_peers[peer.mac] < 5:
                print("Sending question")
                enow.send(QUESTION_BYTES, peer)
                known_peers[peer.mac] += 1
            else:
                enow.peers.remove(peer)
                del known_peers[peer.mac]

        await asyncio.sleep(2)


async def main():
    # Init espnow with broadcast
    enow = espnow.ESPNow()

    listener_task = asyncio.create_task(listener(enow))
    sender_task = asyncio.create_task(sender(enow))

    print("Running...")
    await asyncio.gather(listener_task, sender_task)


asyncio.run(main())
