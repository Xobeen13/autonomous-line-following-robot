import cv2 as cv
import numpy as np

class BlueTargetVision:
    def __init__(self, frame_w=480, frame_h=480, trigger_row=380, min_pixels=40,
                 h_lo=90, h_hi=130, s_lo=130, v_lo=130, median_blur_ksize=5):
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.trigger_row = trigger_row
        self.min_pixels = min_pixels
        self.median_blur_ksize = median_blur_ksize
        self.lower = np.array([h_lo, s_lo, v_lo], dtype=np.uint8)
        self.upper = np.array([h_hi, 255, 255], dtype=np.uint8)

    def detect(self, frame_bgr):
        frame = cv.resize(frame_bgr, (self.frame_w, self.frame_h), interpolation=cv.INTER_AREA)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, self.lower, self.upper)
        if self.median_blur_ksize and self.median_blur_ksize >= 3:
            mask = cv.medianBlur(mask, self.median_blur_ksize)
        y = int(np.clip(self.trigger_row, 0, self.frame_h - 1))
        count = int(np.sum(mask[y, :] == 255))
        return count >= self.min_pixels, {
            "frame": frame, "mask": mask, "trigger_row": y, "count": count
        }
