import numbers
import random
from enum import Enum
from ssl import OPENSSL_VERSION
from getch import get_command
import ansi

BOMBCHAR = "○"
FIREDBOMBCHAR = "◙"
EMPTYCHAR = " "
FLAGCHAR = "●"
WRONGFLAGCHAR = "◘"
CLOSEDCHAR = "."


class MineField:
    def __init__(self, n_rows=10, n_cols=15, mine_probability=0.2):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.mine_probability = mine_probability
        self.finished = False
        self.result = None
        self.init_bombs()
        self.init_numbers()
        self.flags = [[0] * self.n_cols for i in range(self.n_rows)]
        self.open = [[0] * self.n_cols for i in range(self.n_rows)]
        self.fired_bomb_at = None

    def positions(self):
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                yield r, c

    def neighbors(self, r, c):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr = r + dr
                nc = c + dc
                if self.coors_in_field(nr, nc):
                    yield nr, nc

    def init_bombs(self):
        self.bombs = [
            [random.random() < self.mine_probability for c in range(self.n_cols)]
            for r in range(self.n_rows)
        ]

    def init_numbers(self):
        self.numbers = [[0] * self.n_cols for i in range(self.n_rows)]
        for r, c in self.positions():
            self.numbers[r][c] = self.count_neighboring_bombs(r, c)

    @property
    def cells_to_open(self):
        return sum(
            not self.open[r][c] for r, c in self.positions() if not self.bombs[r][c]
        )

    @property
    def n_bombs(self):
        return sum(sum(row) for row in self.bombs)

    @property
    def remaining_bombs(self):
        n_flagged = sum(self.flags[r][c] for r, c in self.positions())
        return self.n_bombs - n_flagged

    def format_cell(self, r, c):
        return (
            self.format_open_cell(r, c)
            if self.open[r][c]
            else self.format_closed_cell(r, c)
        )

    def format_open_cell(self, r, c):
        if self.bombs[r][c]:
            if self.flags[r][c]:
                return FLAGCHAR
            elif self.fired_bomb_at and self.fired_bomb_at == (r, c):
                return FIREDBOMBCHAR
            else:
                return BOMBCHAR
        else:
            if self.flags[r][c]:
                return WRONGFLAGCHAR
            if self.numbers[r][c] > 0:
                return str(self.numbers[r][c])
        return EMPTYCHAR

    def format_closed_cell(self, r, c):
        if self.flags[r][c]:
            return FLAGCHAR
        else:
            return CLOSEDCHAR

    def __str__(self):
        lines = [
            f"Cells to open: {self.cells_to_open}    Bombs to flag: {self.remaining_bombs}    "
        ]
        for r in range(self.n_rows):
            line = []
            for c in range(self.n_cols):
                ch1, ch2 = ("[", "]") if self.focus == (r, c) else (" ", " ")
                line.append(f"{ch1}{self.format_cell(r,c)}{ch2}")
            lines.append("".join(s for s in line))
        lines.append(self.result if self.finished and self.result else "")
        return "\n".join(lines)

    def count_neighboring_bombs(self, r, c):
        n_bombs = 0
        for nr, nc in self.neighbors(r, c):
            if self.bombs[nr][nc]:
                n_bombs += 1
        return n_bombs

    def coors_in_field(self, r, c):
        return 0 <= r < self.n_rows and 0 <= c < self.n_cols

    def open_all(self):
        for r, c in self.positions():
            self.open[r][c] = 1

    def find_empty_cells(self):
        empty_cells = []
        for r, c in self.positions():
            if self.bombs[r][c]:
                continue
            if self.numbers[r][c]:
                continue
            empty_cells.append((r, c))
        return empty_cells

    def open_empty_cell(self):
        empty_cells = self.find_empty_cells()
        self.focus = random.choice(empty_cells)
        self.open_cell(*self.focus)

    def open_cell(self, r, c):
        to_open = [(r, c)]
        while to_open:
            r, c = to_open.pop(0)
            if self.open[r][c]:
                continue
            if self.flags[r][c]:
                continue
            if self.bombs[r][c]:
                self.finished = True
                self.fired_bomb_at = (r, c)
                self.result = "BOOOOOOOM!!! You lost."
                self.open_all()
                return
            self.open[r][c] = 1
            if self.numbers[r][c] == 0:
                for nr, nc in self.neighbors(r, c):
                    to_open.append((nr, nc))

    def open_all_neighbors(self, r, c):
        for r, c in self.neighbors(r, c):
            if not self.open[r][c]:
                self.open_cell(r, c)

    def count_flags_around(self, r, c):
        return sum(self.flags[nr][nc] for nr, nc in self.neighbors(r, c))

    def process(self, command):
        r, c = self.focus
        match command:
            case "up":
                if r - 1 >= 0:
                    self.focus = (r - 1, c)
            case "down":
                if r + 1 < self.n_rows:
                    self.focus = (r + 1, c)
            case "left":
                if c - 1 >= 0:
                    self.focus = (r, c - 1)
            case "right":
                if c + 1 < self.n_cols:
                    self.focus = (r, c + 1)
            case "flag":
                self.flags[r][c] = 0 if self.flags[r][c] else 1
            case "space":
                if self.open[r][c] and self.numbers[r][c] > 0:
                    if self.numbers[r][c] == self.count_flags_around(r, c):
                        self.open_all_neighbors(r, c)
                else:
                    self.open_cell(r, c)
        if not self.finished and self.cells_to_open == 0:
            self.finished = True
            self.result = "YUPEEE!!! You won!"


def main():
    field = MineField(15, 20, 0.2)
    field.open_empty_cell()
    print(field, end="")

    while not field.finished:
        command = get_command()
        if command == "quit":
            break
        field.process(command)
        ansi.move_cursor_by(-field.n_rows - 1, -3 * field.n_cols)
        print(field, end="")


if __name__ == "__main__":
    main()
