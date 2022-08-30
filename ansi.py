import os

os.system("")  # enables ansi escape characters in terminal

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}


def move_cursor_by(dr, dc):
    if dr < 0:
        # Move the cursor up N lines:
        print("\033[{}A".format(-dr), end="")
    elif dr > 0:
        # Move the cursor down N lines:
        print("\033[{}B".format(dr), end="")
    if dc > 0:
        # Move the cursor forward N columns:
        print("\033[{}C".format(dc), end="")
    elif dc < 0:
        # Move the cursor backward N columns:
        print("\033[{}D".format(-dc), end="")


if __name__ == "__main__":
    print(COLOR["GREEN"], "Testing Green", COLOR["ENDC"], sep="", end="")
    move_cursor_by(-3, -2)
    print(COLOR["RED"], "After move", COLOR["ENDC"], sep="")
