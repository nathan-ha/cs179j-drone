import curses
import time


def main(stdscr):
    curses.cbreak()
    stdscr.nodelay(True)  # Non-blocking input
    direction = None
    try:
        while True:
            key = stdscr.getch()
            if key == ord('d'):
                direction = "RIGHT"
            elif key == ord('a'):
                direction = "LEFT"
            else:
                direction = None

            if direction:
              print(direction)

            time.sleep(0.05)  # small delay
    except KeyboardInterrupt:
        pass
    finally:
      curses.wrapper(main)

