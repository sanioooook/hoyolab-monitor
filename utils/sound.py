import time
import winsound


def play_sound(frequency, duration, count):
    for _ in range(count):
        winsound.Beep(frequency, duration)
        time.sleep(0.3)
