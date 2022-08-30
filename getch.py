import sys

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError("getch not available")
    else:
        getch = msvcrt.getch
else:

    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character.
        Nothing is echoed to the console. This call will block if a keypress
        is not already available, but will not wait for Enter to be pressed.

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


ch2dir = {
    b"\r": "return",
    b" ": "space",
    b"a": "left",
    b"d": "right",
    b"w": "up",
    b"s": "down",
    b"f": "flag",
    b"q": "quit",
    b"\xe0": {b"K": "left", b"M": "right", b"H": "up", b"P": "down"},
    b"\x00": {b"K": "left", b"M": "right", b"H": "up", b"P": "down"},
    "\r": "return",
    " ": "space",
    "a": "left",
    "d": "right",
    "w": "up",
    "s": "down",
    "f": "flag",
    "q": "quit",
    "\x1b": {"[": {"A": "up", "B": "down", "C": "right", "D": "left"}},
}


def get_command(char2dir=ch2dir):
    direction = ""
    while not direction:
        ch = getch()
        try:
            direction = char2dir[ch]
        except KeyError:
            # Pressed a key not assigned to any direction
            direction = ""
            continue
        # Pressed a key assigned to direction
        if isinstance(direction, str):
            return direction
        else:
            # direction is a dict for resolving 'more-byte' keystrokes
            return get_command(direction)


if __name__ == "__main__":
    while True:
        ch = getch()
        print(type(ch))
        if ch.isprintable():
            print(ch, ":", ord(ch))
        else:
            print(" ", ":", ord(ch))
        if ch == "q":
            break
