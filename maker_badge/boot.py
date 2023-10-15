import supervisor
import board
import digitalio
import storage


# Workaround for
# https://github.com/adafruit/circuitpython/issues/8449
supervisor.runtime.autoreload = False


switch = digitalio.DigitalInOut(board.D17)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Remount filesystem to write to it
# Keep `-` pressed to update code
print("Filesystem readonly by host:", switch.value)
storage.remount("/", not switch.value)
