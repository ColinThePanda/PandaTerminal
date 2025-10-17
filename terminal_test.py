from src.panda_terminal import Terminal
from panda_math import ivec2

with Terminal(True) as term:
    term.move_cursor(ivec2(0, 5))
    input("Test")
    