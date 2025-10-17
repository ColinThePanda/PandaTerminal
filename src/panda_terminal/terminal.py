from __future__ import annotations
import sys
import os
import ctypes
from panda_math import ivec2


class Cursor:
    def __init__(self, term: Terminal):
        self._handle = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        self._pos = self._get_pos()
        self._term = term

    def _get_pos(self):
        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        class SMALL_RECT(ctypes.Structure):
            _fields_ = [
                ("Left", ctypes.c_short),
                ("Top", ctypes.c_short),
                ("Right", ctypes.c_short),
                ("Bottom", ctypes.c_short),
            ]

        class CSBI(ctypes.Structure):
            _fields_ = [
                ("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", ctypes.c_ushort),
                ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD),
            ]

        csbi = CSBI()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
            self._handle, ctypes.byref(csbi)
        )
        return ivec2(csbi.dwCursorPosition.X, csbi.dwCursorPosition.Y)

    @property
    def pos(self):
        return self._get_pos()

    def move(self, value):
        self._pos = ivec2(value)
        self._pos.x = max(self._pos.x, 0)
        self._pos.y = max(self._pos.y, 0)
        terminal_size = ivec2(self._term.size)
        self._pos.x = min(self._pos.x, terminal_size.x)
        self._pos.y = min(self._pos.y, terminal_size.y)

        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        ctypes.windll.kernel32.SetConsoleCursorPosition(
            self._handle, COORD(int(self._pos.x), int(self._pos.y))
        )

    def update_pos(self):
        self._term.ansi(f"[{self.pos.y};{self.pos.x}]")


class Terminal:
    def __init__(self, seperate: bool) -> None:
        self._show_cursor: bool = True
        self.seperate = seperate
        self._cursor = Cursor(self)

    def __enter__(self):
        if self.seperate:
            self.ansi("[?1049h")  # new win
        self.clear()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ansi("[?25h")  # show cursor
        self.ansi("[?1049l")  # origninal window

    def ansi(self, ansi: str):
        sys.stdout.write(f"\033{ansi}")
        sys.stdout.flush()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    @property
    def size(self) -> ivec2:
        return ivec2(os.get_terminal_size())

    @property
    def show_cursor(self) -> bool:
        return self._show_cursor

    @show_cursor.setter
    def show_cursor(self, value: bool):
        if value == True:
            self.ansi("[?25h")
        else:
            self.ansi("[?25l")

    @property
    def cursor_pos(self) -> ivec2:
        return self._cursor.pos

    def move_cursor(self, position: ivec2):
        self._cursor.move(position)
