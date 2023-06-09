import asyncio

import espnow
import json
import screens
import led
import sleep

import gc

gc.collect()

BROADCAST_PEER = espnow.Peer(b"\xff" * 6)

current_peer = None


def init():
    # Init espnow with broadcast
    enow = espnow.ESPNow()
    enow.peers.append(BROADCAST_PEER)
    return enow


def send_beacon(enow, lang="cz"):
    enow.send(lang.encode("utf-8"), BROADCAST_PEER)


async def right_answer(btn, btns, leds, word_length, secret_char, char_position):
    while True:
        if btn.value:
            led.blink(leds, "green", 1, 0.1)

            letters = screens.load_letters()
            letters["letters"][char_position] = secret_char
            letters["key_len"] = word_length
            screens.save_letters(letters)

            sleep.sleep(btns)
        await asyncio.sleep(0.05)


async def wrong_answer(active_btns, btns, leds):
    while True:
        for i in active_btns:
            if btns[i].value:
                led.blink(leds, "red", 1, 0.1)
                sleep.sleep(btns)
        await asyncio.sleep(0.05)


async def listener(enow, display, buttons, lang, leds):
    global current_peer
    while True:
        if enow:
            packet = enow.read()
            print("Packet", packet.mac, packet.msg, packet.rssi)

            if not current_peer:
                current_peer = packet.mac

            question = json.loads(packet.msg.decode("utf-8"))
            # Format: (
            #   0: question,
            #   1: (answers), # At most 5 answers
            #   2: correct_answer_index,
            #   3: secret_char,
            #   4: secret_char_position,
            #   5: word_length
            # )
            screens.display_question_screen(display, question, lang)

            correct_answer = question[2]
            answers_len = len(question[1])

            asyncio.create_task(
                right_answer(
                    buttons[correct_answer],
                    buttons,
                    leds,
                    word_length=question[5],
                    secret_char=question[3],
                    char_position=question[4],
                )
            )

            asyncio.create_task(
                wrong_answer((i for i in range(answers_len) if i != correct_answer), buttons, leds)
            )

        await asyncio.sleep(0)
