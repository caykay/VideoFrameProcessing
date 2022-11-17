# Helper class that tells time
import time


class Timer:
    def __init__(self):
        self._start = 0
        self._end = 0
        self._active = False

    def start(self):
        """Starts the timer"""
        if self._active:
            print("There already is an active timer")
        else:
            self._active = True
            self._start = time.perf_counter()

    def stop(self):
        """Stops the timer"""
        if self._active:
            self._end = time.perf_counter()
        self._active = False

    def elapsedTime(self):
        """Returns the time elapsed.
        Will still return time elapsed so far even when timer is not stopped"""
        return f"{(time.perf_counter() - self._start):.2f}" if self._end == 0 else f"{(self._end - self._start):.2f}"
