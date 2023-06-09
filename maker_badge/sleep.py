import alarm
import board
import button


def sleep(btns):
    button.deinit(btns)
    pin_alarm = alarm.pin.PinAlarm(board.D0, value=False, pull=False)
    alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
