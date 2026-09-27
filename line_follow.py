"""
Reconstructed scaffold: original line-following code was not fully preserved.
"""
import cv2 as cv
import numpy as np

class RedLineFollower:
    def __init__(self, frame_w=480, frame_h=480, base_pwm=120, steering_gain=0.5):
        self.frame_w = frame_w
        self.frame_h = frame_h
        self.base_pwm = base_pwm
        self.steering_gain = steering_gain

    def step(self, frame_bgr):
        frame = cv.resize(frame_bgr, (self.frame_w, self.frame_h))
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        m1 = cv.inRange(hsv, np.array([0,100,80]), np.array([10,255,255]))
        m2 = cv.inRange(hsv, np.array([170,100,80]), np.array([179,255,255]))
        mask = m1 | m2
        roi = mask[int(self.frame_h*0.55):, :]
        M = cv.moments(roi)
        if M["m00"] == 0:
            return 0, 0, {"line_found": False, "mask": mask}
        cx = int(M["m10"]/M["m00"])
        error = cx - self.frame_w//2
        correction = int(self.steering_gain * error)
        left = int(np.clip(self.base_pwm + correction, -255, 255))
        right = int(np.clip(self.base_pwm - correction, -255, 255))
        return left, right, {"line_found": True, "mask": mask, "cx": cx, "error": error}
