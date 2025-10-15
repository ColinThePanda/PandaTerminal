import sys
import os
import ctypes
from panda_math import ivec2


def ansi(ansi: str):
    sys.stdout.write(f"\033{ansi}")
    sys.stdout.flush()


def new_window():
    ansi("[?1049h")


def original_window():
    ansi("[?104l")


def hide_cursor():
    ansi("[?25l")


def show_cursor():
    ansi("[?25h")


def get_terminal_size():
    return ivec2(os.get_terminal_size())


class Cursor:
    def __init__(self):
        self._handle = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        self._pos = self._get_pos()

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
    def position(self):
        return self._get_pos()

    @position.setter
    def position(self, value):
        self._pos = ivec2(value)
        self._pos.x = max(self._pos.x, 0)
        self._pos.y = max(self._pos.y, 0)
        terminal_size = ivec2(get_terminal_size())
        self._pos.x = min(self._pos.x, terminal_size.x)
        self._pos.y = min(self._pos.y, terminal_size.y)

        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

        ctypes.windll.kernel32.SetConsoleCursorPosition(
            self._handle, COORD(int(self._pos.x), int(self._pos.y))
        )

    def update_pos(self):
        ansi(f"[{self.position.y};{self.position.x}]")


class Window:
    def __init__(self, show_cursor: bool = True):
        self.cursor: Cursor = Cursor()
        self._show_cursor = show_cursor

    @property
    def show_cursor(self):
        return self._show_cursor

    @show_cursor.setter
    def show_cursor(self, value: bool):
        if value:
            self._show_cursor = True
            show_cursor()
        else:
            self._show_cursor = False
            hide_cursor()

    @property
    def size(self) -> ivec2:
        return ivec2(get_terminal_size())

    def __enter__(self):
        if not self.show_cursor:
            hide_cursor()
        new_window()
        self.clear()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.show_cursor:
            show_cursor()
        original_window()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")
