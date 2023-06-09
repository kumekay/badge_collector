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
#   question, # max 40 symbols
#   (answers), # At most 5 answers, 7 symbols
#   correct_answer_index,
#   secret_char,
#   secret_char_position,
#   word_length
# )

KEY = [
    1,  # correct_answer_index
    "k",  # secret_char
    2,  # secret_char_position
    4,  # word_length
]


QUESTION_EN = [
    "The first Espressif chip is ...",  # question
    (  # answers
        "ESP32",
        "ESP8266",
        "ESP16",
        "ESP32-C3",
    ),
] + KEY


QUESTION_CZ = [
    "Prvni cip Espressif je ...",  # question
    (
        "ESP32",
        "ESP8266",
        "ESP16",
        "ESP32-C3",
    ),
] + KEY


QUESTION_BYTES_EN = json.dumps(QUESTION_EN).encode("utf-8")
QUESTION_BYTES_CZ = json.dumps(QUESTION_CZ).encode("utf-8")


async def listener(enow):
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)
            lang = packet.msg.decode("utf-8")
            # If we don't know this peer, add it to the dictionary
            if lang in ["cz", "en"] and packet.mac not in current_peers:
                print(
                    "New peer found:",
                    packet.mac,
                )
                enow.peers.append(espnow.Peer(packet.mac))
                save_peers(packet.mac)
                current_peers[packet.mac] = [0, lang]

        await asyncio.sleep(0)


async def sender(enow):
    while True:
        # Send question to all known peers 3 times, then remove them from the list
        for peer in enow.peers:
            if current_peers[peer.mac][0] < 3:
                lang = current_peers[peer.mac][1]
                print("Sending question", lang)
                enow.send(
                    QUESTION_BYTES_CZ if lang == "cz" else QUESTION_BYTES_EN,
                    peer,
                )
                current_peers[peer.mac][0] += 1
            else:
                enow.peers.remove(peer)
                del current_peers[peer.mac]

        await asyncio.sleep(1)


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
