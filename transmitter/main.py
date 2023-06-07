import asyncio
import binascii
import json

import espnow

# Dictionary of known peers
# Keys are MAC addresses, values - number of packets sent
current_peers = {}

# List of all peers ever seen
all_peers = []  # type: list[str]

# Question to be sent
# Format: (
#   question,
#   (answers), # At most 5 answers
#   correct_answer_index,
#   secret_char,
#   secret_char_position,
#   word_length
# )
QUESTION = (
    "The first ESP chip is ...",
    (
        "ESP32",
        "ESP8266",
        "ESP2413",
        "ESP32-C3",
        "ESP16",
    ),
    1,
    "E",
    2,
    7,
)
QUESTION_BYTES = json.dumps(QUESTION).encode("utf-8")


async def listener(enow):
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)

            # If we don't know this peer, add it to the dictionary
            if packet.msg == b"makers!" and packet.mac not in current_peers:
                print("New peer found:", packet.mac)
                enow.peers.append(espnow.Peer(packet.mac))
                save_peers(packet.mac)
                current_peers[packet.mac] = 0

        await asyncio.sleep(0)


async def sender(enow):
    while True:
        # Send question to all known peers 5 times, then remove them from the list
        for peer in enow.peers:
            if current_peers[peer.mac] < 5:
                print("Sending question")
                enow.send(QUESTION_BYTES, peer)
                current_peers[peer.mac] += 1
            else:
                enow.peers.remove(peer)
                del current_peers[peer.mac]

        await asyncio.sleep(2)


def save_peers(mac):
    global all_peers

    if mac not in all_peers:
        all_peers.append(binascii.hexlify(mac))
        with open("/peers.json", "w") as f:
            json.dump(all_peers, f)


async def main():
    global all_peers
    with open("/peers.json", "r") as f:
        all_peers = json.load(f)

    # Init espnow with broadcast
    enow = espnow.ESPNow()

    listener_task = asyncio.create_task(listener(enow))
    sender_task = asyncio.create_task(sender(enow))

    print("Running...")
    await asyncio.gather(listener_task, sender_task)


asyncio.run(main())
