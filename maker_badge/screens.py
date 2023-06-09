import asyncio

from display import build_display_data, draw_badge, draw_key, draw_question, show
import json
import gc

gc.collect()


def load_letters():
    # Example json:
    # {"letters": {0: "m", 3: "a"}, "key_len": 4}
    with open("/letters.json", "r") as f:
        return json.load(f)


def save_letters(letters):
    with open("/letters.json", "w") as f:
        json.dump(letters, f)


def show_letters(display_data, lang):
    letters = load_letters()
    draw_key(
        display_data,
        known_letters=letters.get("letters", {}),
        key_len=letters.get("key_len", 0),
        lang=lang,
    )


def display_question_screen(display, packet, lang):
    # Format: (
    #   0: question,
    #   1: (answers), # At most 5 answers
    #   2: correct_answer_index,
    #   3: secret_char,
    #   4: secret_char_position,
    #   5: word_length
    # )

    display_data = build_display_data()
    draw_question(display_data, packet[0], packet[1])
    show_letters(display_data, lang)
    asyncio.create_task(show(display, display_data))

    # Create button handler


async def display_badge_screen(display, name, company, awake, lang):
    display_data = build_display_data()
    show_letters(display_data, lang)
    draw_badge(display_data, name, company, awake, lang)
    await show(display, display_data)
