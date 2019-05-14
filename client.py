import recogniser.face_recogniser
import screenshot.screenshoter
import active_proc
import dawn_mode
import time
import threading


def f():
    time_hist = dict()
    prev_active = active_proc.get_active_window()
    start = time.time()
    while True:
        active_window = active_proc.get_active_window()
        if prev_active != active_window:
            finish = time.time()
            if prev_active in time_hist.keys():
                time_hist[prev_active] += finish - start
            else:
                time_hist[prev_active] = finish - start
            start = finish
            prev_active = active_window
        time.sleep(5)
