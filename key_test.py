from src.panda_terminal import read_key, Key

key = read_key()

match key:
    case Key.SPACE:
        print("You pressed space")
    case Key.ENTER:
        print("You pressed enter")
    case _:
        print(f"You pressed {key}")