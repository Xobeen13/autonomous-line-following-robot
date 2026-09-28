"""
Reconstructed high-level controller based on the surviving project notes.
"""
import time
import cv2 as cv
from line_follow import RedLineFollower
from blue_detection import BlueTargetVision
from green_detection import GreenDetector
from turn180 import Turn180
from pickup_action import PickupAction
from io_i2c import I2CDriver

def main():
    cap = cv.VideoCapture(0)
    follower = RedLineFollower()
    blue = BlueTargetVision()
    green = GreenDetector()
    turn = Turn180()
    pickup = PickupAction()

    try:
        driver = I2CDriver()
    except Exception as exc:
        print(f"[WARN] I2C unavailable: {exc}")
        driver = None

    state = "FOLLOW_TO_PICKUP"

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            now = time.time()

            if state == "FOLLOW_TO_PICKUP":
                hit, _ = blue.detect(frame)
                if hit:
                    if driver: driver.stop()
                    pickup.start(now)
                    state = "PICKUP"
                else:
                    l, r, _ = follower.step(frame)
                    if driver: driver.send(l, r)

            elif state == "PICKUP":
                if pickup.step(driver, now):
                    turn.start(now)
                    state = "TURN_180"

            elif state == "TURN_180":
                l, r, done = turn.step(now)
                if driver: driver.send(l, r)
                if done:
                    state = "FOLLOW_TO_DROPOFF"

            elif state == "FOLLOW_TO_DROPOFF":
                hit, _ = green.detect(frame)
                if hit:
                    if driver:
                        driver.stop()
                        driver.send_dropoff()
                    state = "DONE"
                else:
                    l, r, _ = follower.step(frame)
                    if driver: driver.send(l, r)

            elif state == "DONE":
                if driver: driver.stop()
                print("Mission complete.")
                break

            cv.imshow("Robot Camera", frame)
            if cv.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv.destroyAllWindows()
        if driver:
            driver.stop()
            driver.close()

if __name__ == "__main__":
    main()
