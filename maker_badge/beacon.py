import asyncio

import espnow
import json
import screens
import led
import sleep
from state import g
import gc

gc.collect()

BROADCAST_PEER = espnow.Peer(b"\xff" * 6)

g.current_peer = None


def init():
    # Init espnow with broadcast
    enow = espnow.ESPNow()
    enow.peers.append(BROADCAST_PEER)
    return enow


def send_beacon(lang="cz"):
    g.enow.send(lang.encode("utf-8"), BROADCAST_PEER)


async def right_answer(btn, word_length, secret_char, char_position):
    while True:
        if btn.value:
            asyncio.create_task(led.blink("green", 1, 0.2))

            screens.load_letters()
            g.letters["letters"][char_position] = secret_char
            g.letters["key_len"] = word_length
            screens.save_letters()

            await sleep.sleep()
        await asyncio.sleep(0.05)


async def wrong_answer(btn):
    while True:
        if btn.value:
            asyncio.create_task(led.blink("red", 1, 0.1))
            await sleep.sleep()
        await asyncio.sleep(0.05)


async def listener(lang):
    enow = g.enow
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)

            if g.current_peer:
                continue

            g.current_peer = packet.mac

            question = json.loads(packet.msg.decode("utf-8"))
            # Format: (
            #   0: question,
            #   1: (answers), # At most 5 answers
            #   2: correct_answer_index,
            #   3: secret_char,
            #   4: secret_char_position,
            #   5: word_length
            # )
            screens.display_question_screen(question, lang)

            correct_answer = question[2]
            answers_len = len(question[1])

            for i in range(answers_len):
                if i == correct_answer:
                    asyncio.create_task(
                        right_answer(
                            g.buttons[correct_answer],
                            word_length=question[5],
                            secret_char=question[3],
                            char_position=question[4],
                        )
                    )
                else:
                    asyncio.create_task(wrong_answer(g.buttons[i]))

        await asyncio.sleep(0)
