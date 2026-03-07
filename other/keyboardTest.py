import sys
import select
import termios
import atexit
import time

# Save original terminal settings
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

# Restore terminal settings on exit
def restore_terminal():
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

atexit.register(restore_terminal)

# Put terminal in raw mode (so we can read keys immediately)
new_settings = termios.tcgetattr(fd)
new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)  # Disable canonical mode and echo
termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)

def get_key():
    dr, dw, de = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

try:
    while True:
        key = get_key()
        if key == 'a':
            print("LEFT")
        elif key == 'd':
            print("RIGHT")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("Exiting...")