# credit from https://techtutorialsx.com/2021/04/29/python-opencv-splitting-video-frames/amp/
import cv2
from helper import Timer
from skimage.metrics import structural_similarity as ssim

timer = Timer()
frame_id = 0
images = []

capture = cv2.VideoCapture('sampleClips/video.mp4')

while True:
    success, frame = capture.read()
    if not success:
        break

    images.append((frame_id, frame))
    frame_id += 1
    # TODO: future implementations for frame processing

# print(f"Getting frames: Elapsed time {timer.elapsedTime()}")
# print(f"Frames per second {capture.get(cv2.CAP_PROP_FPS)}")
# Adding frames to given file
# for id, frame in images:
#     cv2.imwrite(f'SplitFrames/1/frame {id}.jpg', frame)

capture.release()
# if __name__ == '__main__':
#     pass


def remove_dupe_frames(frames, max_sim = 0.95):
    """Remove duplicate frames among the generated frames"""

