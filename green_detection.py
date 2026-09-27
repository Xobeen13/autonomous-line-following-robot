"""
Reconstructed scaffold: original green detector was only partially preserved.
"""
import cv2 as cv
import numpy as np

class GreenDetector:
    def __init__(self, frame_w=480, frame_h=480, min_pixels=4000,
                 h_lo=35, h_hi=85, s_lo=80, v_lo=80):
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.min_pixels = min_pixels
        self.lower = np.array([h_lo, s_lo, v_lo], dtype=np.uint8)
        self.upper = np.array([h_hi, 255, 255], dtype=np.uint8)

    def detect(self, frame_bgr):
        frame = cv.resize(frame_bgr, (self.frame_w, self.frame_h))
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, self.lower, self.upper)
        count = int(np.count_nonzero(mask))
        return count >= self.min_pixels, {"frame": frame, "mask": mask, "count": count}
