import alarm
import board
import button
from state import g
from screens import display_badge_screen, load_letters


async def sleep():
    load_letters()
    await display_badge_screen(g.name, g.company, lang=g.lang, awake=False)
    button.deinit(g.buttons)
    pin_alarm = alarm.pin.PinAlarm(board.D0, value=False, pull=False)
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
