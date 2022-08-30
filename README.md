# Terminal Minesweeper

Terminal minesweeper in Python. Inspired by [Alexey Kutepov's VOD](https://www.youtube.com/watch?v=8UJNQt8DAWE&t=6711s) ([source code in Pascal](https://github.com/tsoding/mine)).

Tested with Python 3.8 on Windows 10 (PowerShell), and on Ubuntu 20.04.4 LTS running on Windows under WSL. Uses Unicode chars to represent flags and bombs. (Older terminals, e.g. CMD on Windows, may not support them.)

```
MINESWEEPER!
Controls: Q - quit, WASD or cursor keys - move focus, F - toggle flag, SPACE - open cell
Cells to open: 0    Bombs to flag: 55
 1  ○  ○  ○  1                    1  ○  1           1  ○  1
 2  4  ○  3  1                    1  1  1           1  1  1
 1  ○  2  1                    1  1  2  1  2  1  1
 2  2  2        1  2  2  2  1  2  ○  2  ○  3  ○  2  1  1  1
 1  ○  1        1  ○  ○  2  ○  3  3  3  3  5  ○  3  1  ○  1
 3  3  3  1  1  1  2  2  2  3  ○  4  ○  2  ○  ○  2  1  2  2
 ○  ○  2  ○  1              2  ○  ○  2  3  3  3  2  1  3  ○
 2  2  2  1  1        1  2  3  4  3  3  2  ○  1  2  ○  4  ○
 2  2  1              1  ○  ○  2 [◙] 2  ●  2  2  4  ○  5  2
 ○  ○  2  1  1  1  1  2  3  2  2  2  3  2  1  2  ●  ○  4  ○
 3  ○  4  3  ○  1  2  ○  3  1     1  ●  1     3  ●  ○  4  2
 2  3  ○  ○  2  1  2  ○  ○  2  1  2  1  1     2  ●  4  ○  2
 ○  2  2  2  1     1  2  3  4  ●  3  1     1  2  2  2  2  ○
 2  3  2  1              2  ○  ●  ●  2  1  2  ●  2  1  1  1
 1  ○  ○  1              2  ○  5  ○  2  1  ○  3  ○  1
BOOOOOOOM!!! You lost.
```

## Quick Start

```console
$ python ./mine.py
```

## Controls

| key                                                 | description        |
|-----------------------------------------------------|--------------------|
| <kbd>w</kbd>,<kbd>a</kbd>,<kbd>s</kbd>,<kbd>d</kbd> | Move cursor around |
| <kbd>↑</kbd>,<kbd>←</kbd>,<kbd>↓</kbd>,<kbd>→</kbd> | Move cursor around |
| <kbd>SPACE</kbd>                                    | Open cell          |
| <kbd>f</kbd>                                        | Flag/unflag cell   |
| <kbd>q</kbd>                                        | Quit               |
