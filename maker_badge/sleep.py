import alarm
import board


def sleep():
    pin_alarm = alarm.pin.PinAlarm(board.D0, value=False)
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
