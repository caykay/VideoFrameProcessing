# credit from https://techtutorialsx.com/2021/04/29/python-opencv-splitting-video-frames/amp/
import cv2
from helper import Timer, remove_dupe_frames, plot_frames
from skimage.metrics import structural_similarity as ssim

capture = cv2.VideoCapture('sampleClips/5_seconds_cntdown.mp4')
timer = Timer()
images = []
gs_frames = []

timer.start()
while True:
    success, frame = capture.read()
    if not success:
        break

    images.append(frame)
    # Frame processing
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gs_frames.append(gray_frame)
timer.stop()

print(f"Splitting frames: Elapsed time {timer.elapsedTime()}")
print(f"FPS: {capture.get(cv2.CAP_PROP_FPS)}\n"
      f"Frame count: {capture.get(cv2.CAP_PROP_FRAME_COUNT)}")

capture.release()

# grayscale frames only
unique_frames = remove_dupe_frames(gs_frames, timer)

# plot unique frames
plot_frames(unique_frames, timer)
