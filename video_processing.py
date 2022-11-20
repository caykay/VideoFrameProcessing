import cv2
import queue
from threading import Thread


class VideoProcessor:
    def __init__(self, video_path: str, queue_size=128, gray_scale = True):
        self.capture = cv2.VideoCapture(video_path)
        self.stopped = False
        self.gs = gray_scale
        self.fr_queue = queue.Queue(maxsize=queue_size)
    
    def start(self):
        # creates a thread to execute the update function
        # no arguments passed
        thread = Thread(target=self.update)
        thread.daemon = True
        thread.start()
        return self
    
    def stop(self):
        self.stopped = True
    
    def read(self):
        """"""      
        # risk of deadlock when waiting
        return self.fr_queue.get(block=(not self.stopped))

    def has_more_frames(self):
        # return self.fr_queue.qsize() > 0
        if self.fr_queue.qsize() > 0:
            return True
        else:
            if self.stopped:
                return False
            else:
                return True
        # return self.fr_queue.qsize() > 0

    def update(self):     
        while True:
            if self.stopped:
                return

            if not self.fr_queue.full():
                success, frame = self.capture.read()
                if not success:
                    self.stop()
                    return

                self.fr_queue.put(frame)
        