import board
import digitalio
import storage

switch = digitalio.DigitalInOut(board.BUTTONS)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# Remount filesystem to write to it
# Keep `-` pressed to update code
print("Filesystem readonly by host:", switch.value)
storage.remount("/", not switch.value)
