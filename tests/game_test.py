from panda_terminal import Terminal, read_key, Key
from panda_math import ivec2
import time

pos = ivec2(5, 5)

with Terminal(double_buffer=True) as term:
    term.show_cursor = False
    while True:
        term.clear()

        char = "▒"
        for y in range(term.size.y):
            term.write(0, y, char * term.size.x)

        term.write(int(pos.x * 2), int(pos.y), "██")

        term.render()
        
        #time.sleep(0.16)

        key = read_key()
        match key:
            case Key.UP:
                pos.y -= 1
            case Key.DOWN:
                pos.y += 1
            case Key.LEFT:
                pos.x -= 1
            case Key.RIGHT:
                pos.x += 1
        pos.y = max(0, min(pos.y, term.size.y))
        pos.x = max(0, min(pos.x, term.size.x))
