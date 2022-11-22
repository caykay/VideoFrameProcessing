# credit from https://techtutorialsx.com/2021/04/29/python-opencv-splitting-video-frames/amp/
import cv2
from helper import Timer, remove_dupe_frames, plot_frames
from video_processing import VideoProcessor
from skimage.metrics import structural_similarity as ssim
import time
import ray
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from collections import deque

# ray.init(num_cpus = 10)

path = 'sampleClips/video.mp4'

capture = cv2.VideoCapture(path)
timer = Timer()
frames = []
gs_frames = []

timer.start()
while True:
    success, frame = capture.read()
    if not success:
        break

    # frames.append(frame)
    # Frame processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gs_frames.append(gray_frame)
timer.stop()
print(f"Splitting frames in single thread: Elapsed time {timer.elapsedTime()}\n\
    Frames: {len(gs_frames)}")

gs_frames = []
capture = cv2.VideoCapture(path)

def get_gray_scale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

thread_n = cv2.getNumberOfCPUs()
pool = ThreadPool(processes = thread_n)
timer.start()
futures = deque()
while True:
    # if len(futures) < thread_n:
    success, frame = capture.read()
    if not success:
        gray_frame = None
        break
    futures.append(pool.apply_async(get_gray_scale, (frame,)))

    # images.append(frame)
    # TODO: future implementations for frame processing
    # frame_id = ray.put(frame)
    # futures.append(get_gray_scale.remote(frame))

# while len(futures) > 0:
#     if len(futures) > 0 and futures[0].ready():
#         result = futures.popleft().get()
#         gs_frames.append(result)
while len(futures) > 0:
    if futures[0].ready():
        gs_frames.append(futures.popleft().get())
timer.stop()

print(f"Splitting frames in pool of thread: Elapsed time {timer.elapsedTime()}\n\
    Frames: {len(gs_frames)}")
pool.close()
pool.join()

# timer.start()
# video = VideoProcessor(path).start()
# time.sleep(0.3)
# while video.has_more_frames():
#     frame = video.read()
#     gs_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

# timer.stop()
# print(f"Splitting frames in external thread: Elapsed time {timer.elapsedTime()}\n\
#     Frames: {len(gs_frames)}")

# print(f"FPS: {capture.get(cv2.CAP_PROP_FPS)}\n"
#       f"Frame count: {capture.get(cv2.CAP_PROP_FRAME_COUNT)}")

# capture.release()

# # grayscale frames only
# unique_frames = remove_dupe_frames(gs_frames, timer)

# # plot unique frames
# plot_frames(unique_frames, col_limit=3)
