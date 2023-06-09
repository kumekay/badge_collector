import asyncio

from display import build_display_data, draw_badge, draw_key, draw_question, show


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
    # TODO: load letters from the json file
    known_letters = {0: "m"}
    draw_key(
        display_data,
        known_letters,
        key_len=packet[5],
        lang=lang,
    )
    asyncio.create_task(show(display, display_data))

    # Create button handler


async def display_badge_screen(display, name, company, awake, lang):
    display_data = build_display_data()
    draw_badge(display_data, name, company, awake, lang)
    await show(display, display_data)
