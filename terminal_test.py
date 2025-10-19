from src.panda_terminal import Terminal
from panda_color import Colors, color_text
import time
import math
import random


def stress_test_1_massive_updates(term: Terminal):
    """Test 1: Massive screen updates - fill entire screen every frame"""
    print("Test 1: Massive Updates (filling entire screen)")
    time.sleep(1)

    start_time = time.time()
    frames = 0
    test_duration = 3.0  # Run for 3 seconds
    chars = ["░", "▒", "▓", "█"]
    colors = [Colors.RED, Colors.GREEN, Colors.BLUE]

    while time.time() - start_time < test_duration:
        term.clear()
        height = term.size.y
        width = term.size.x

        # Fill the entire screen with characters
        char = color_text(chars[frames % 4], colors[frames % 3])
        for y in range(height):
            for x in range(width):
                term.write(x, y, char)

        term.write(5, 5, f"Frame: {frames} - FULL SCREEN UPDATE")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def stress_test_2_random_noise(term: Terminal):
    """Test 2: Random character spam across screen"""
    print("Test 2: Random Noise")
    time.sleep(1)

    chars = "█▓▒░#@%&*+=~"
    start_time = time.time()
    frames = 0
    test_duration = 3.0

    while time.time() - start_time < test_duration:
        term.clear()
        max_x = term.size.x - 1
        max_y = term.size.y - 1

        # Draw 500 random characters
        for _ in range(500):
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            term.write(x, y, random.choice(chars))

        term.write(5, 5, f"Frame: {frames}")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def stress_test_3_many_moving_objects(term: Terminal):
    """Test 3: Many moving objects simultaneously"""
    print("Test 3: Multiple Moving Objects")
    time.sleep(1)

    num_objects = 50
    objects = []

    # Initialize objects
    size = term.size
    for _ in range(num_objects):
        objects.append(
            {
                "x": random.randint(0, size.x - 2),
                "y": random.randint(0, size.y - 2),
                "vx": random.choice([-1, 1]),
                "vy": random.choice([-1, 1]),
                "char": random.choice(["●", "■", "◆", "▲", "▼"]),
            }
        )

    start_time = time.time()
    frames = 0
    test_duration = 3.0

    while time.time() - start_time < test_duration:
        term.clear()
        max_x = term.size.x - 2
        max_y = term.size.y - 2

        # Update and draw all objects
        for obj in objects:
            obj["x"] += obj["vx"]
            obj["y"] += obj["vy"]

            # Bounce off edges
            if obj["x"] <= 0 or obj["x"] >= max_x:
                obj["vx"] *= -1
            if obj["y"] <= 0 or obj["y"] >= max_y:
                obj["vy"] *= -1

            term.write(int(obj["x"]), int(obj["y"]), obj["char"])

        term.write(5, 5, f"Frame: {frames} - {num_objects} objects")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def stress_test_4_sine_wave_animation(term: Terminal):
    """Test 4: Complex mathematical animation"""
    print("Test 4: Sine Wave Animation")
    time.sleep(1)

    start_time = time.time()
    frames = 0
    test_duration = 3.0

    while time.time() - start_time < test_duration:
        term.clear()
        height = term.size.y
        width = term.size.x

        # Draw multiple sine waves - optimized
        frame_offset = frames * 0.1
        for y_offset in range(0, height, 2):
            for x in range(width):
                y = int(y_offset + 5 * math.sin((x * 0.1) + frame_offset))
                if 0 <= y < height:
                    term.write(x, y, "█")

        term.write(5, 2, f"Frame: {frames}")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def stress_test_5_scrolling_text(term: Terminal):
    """Test 5: Heavy text scrolling"""
    print("Test 5: Scrolling Text Wall")
    time.sleep(1)

    text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 10

    start_time = time.time()
    frames = 0
    test_duration = 3.0

    while time.time() - start_time < test_duration:
        term.clear()
        height = term.size.y
        width = term.size.x

        # Draw scrolling text on every line
        for y in range(height):
            offset = (frames * 2 + y * 3) % len(text)
            line = text[offset:] + text[:offset]
            term.write(0, y, line[:width])

        term.write(5, 5, f"[Frame: {frames}]")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def stress_test_6_matrix_effect(term: Terminal):
    """Test 6: Matrix-style falling characters"""
    print("Test 6: Matrix Rain Effect")
    time.sleep(1)

    columns = []
    chars = list("01アイウエオカキクケコサシスセソ")
    last_width = 0

    start_time = time.time()
    frames = 0
    test_duration = 3.0

    while time.time() - start_time < test_duration:
        term.clear()
        height = term.size.y
        width = term.size.x

        # Reinitialize columns if width changed
        if width != last_width:
            columns = []
            for x in range(width):
                columns.append(
                    {
                        "x": x,
                        "y": random.randint(-height, 0),
                        "speed": random.randint(1, 3),
                        "length": random.randint(5, 20),
                    }
                )
            last_width = width

        for col in columns:
            # Draw trail - optimized by pre-selecting characters
            trail_chars = [random.choice(chars) for _ in range(col["length"])]

            for i in range(col["length"]):
                y = col["y"] - i
                if 0 <= y < height:
                    term.write(col["x"], y, trail_chars[i])

            col["y"] += col["speed"]

            # Reset when off screen
            if col["y"] > height + col["length"]:
                col["y"] = -col["length"]
                col["speed"] = random.randint(1, 3)

        term.write(5, 5, f"Frame: {frames}")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def stress_test_7_rapid_clearing(term: Terminal):
    """Test 7: Rapidly clear and redraw"""
    print("Test 7: Rapid Clear/Redraw")
    time.sleep(1)

    start_time = time.time()
    frames = 0
    test_duration = 3.0

    while time.time() - start_time < test_duration:
        term.clear()
        height = term.size.y
        width = term.size.x

        # Draw pattern
        for y in range(height):
            if y % 2 == frames % 2:
                term.write(0, y, "█" * width)

        term.write(5, 5, f"Frame: {frames} - RAPID REDRAW")
        term.render()
        frames += 1

    elapsed = time.time() - start_time
    fps = frames / elapsed
    return fps, frames


def main():
    with Terminal(seperate=True, double_buffer=True) as term:
        term.show_cursor = False

        tests = [
            ("Test 1: Massive Updates", stress_test_1_massive_updates),
            ("Test 2: Random Noise", stress_test_2_random_noise),
            ("Test 3: Moving Objects", stress_test_3_many_moving_objects),
            ("Test 4: Sine Wave Animation", stress_test_4_sine_wave_animation),
            ("Test 5: Scrolling Text", stress_test_5_scrolling_text),
            ("Test 6: Matrix Effect", stress_test_6_matrix_effect),
            ("Test 7: Rapid Clear/Redraw", stress_test_7_rapid_clearing),
        ]

        term.write(5, 5, "=== TERMINAL FPS BENCHMARK ===")
        term.write(5, 7, "Running 7 rendering tests at maximum speed...")
        term.write(5, 8, "Each test runs for 3 seconds")
        term.write(5, 10, "Press Ctrl+C to stop")
        term.render()
        time.sleep(3)

        results = []

        for test_name, test_func in tests:
            try:
                fps, frames = test_func(term)
                results.append((test_name, fps, frames))
            except KeyboardInterrupt:
                break

        # Display results
        term.clear()
        term.write(5, 5, "=== FPS BENCHMARK RESULTS ===")
        term.write(5, 6, "")

        y_pos = 8
        for test_name, fps, frames in results:
            term.write(5, y_pos, f"{test_name:30} {fps:8.2f} FPS  ({frames} frames)")
            y_pos += 1

        if results:
            avg_fps = sum(fps for _, fps, _ in results) / len(results)
            term.write(5, y_pos + 1, f"Average FPS: {avg_fps:.2f}")

        term.write(5, y_pos + 3, "Benchmark complete! Press Ctrl+C to exit")
        term.render()

        # Keep results visible
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
