# Helper class that tells time
import cv2
import time
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim


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


def remove_dupe_frames(frames, timer: Timer, max_sim=0.95, gray_scale=True):
    """Remove duplicate frames among the generated frames"""
    c_frame = frames[0]
    non_dupes = [c_frame]  # we consider the first frame to be the first unique frame

    timer.start()
    for frame in frames[1:]:
        # channel axis
        axis = None if gray_scale else 2

        sim = ssim(frame, c_frame, channel_axis=axis)
        if sim < max_sim:
            # add to unique frames list
            non_dupes.append(frame)
            c_frame = frame
    timer.stop()
    print(f"Removing duplicate frames: {timer.elapsedTime()}")
    return non_dupes


def save_frames_to_file(frames: list, file_name: str, timer: Timer):
    timer.start()
    # Adding frames to given file
    for id, frame in enumerate(frames):
        cv2.imwrite(f'SplitFrames/{file_name}/frame {id}.jpg', frame)
    timer.stop()

    print(f"Saving frames: Elapsed time {timer.elapsedTime()}")


def plot_frames(frames, col_limit=3):
    rows, cols = round(len(frames)/col_limit), col_limit
    fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(5 * cols, 5 * rows))
    rows, cols = axes.shape
    for row in range(rows):
        for col in range(cols):
            if row * cols + col + 1 > len(frames):
                # hide axis if it's not supposed to be plotted
                axes[row][col].set_axis_off()
                break
            axes[row][col].imshow(frames[row * cols + col], cmap=plt.cm.gray)
            axes[row][col].set_title(f"Frame {row * cols + col + 1}")

    # adjust padding btwn subplots
    plt.tight_layout()
    # show plot
    plt.show()
