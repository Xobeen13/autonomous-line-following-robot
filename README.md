# Autonomous Vision-Guided Pickup Robot

An autonomous mobile robot designed to follow a marked course, detect a pickup target, collect a LEGO figure, perform a 180° turn, and navigate to a green drop-off zone using computer vision and embedded control.

## Mission
1. Follow a colored guide line
2. Detect a blue pickup target
3. Stop and trigger pickup
4. Perform a 180° turn
5. Resume navigation
6. Detect a green drop-off zone
7. Trigger drop-off

## Technologies
Python, OpenCV, NumPy, I2C, computer vision, embedded systems, motor control, robotics.

## Repository structure
- `src/` — Python source code
- `images/` — final robot/testing photos
- `design/` — concept sketches and initial drawings

## Reconstruction note
This repository was reconstructed from the code and notes that remained from the original project. `blue_detection.py`, `turn180.py`, `io_i2c.py`, and `pickup_action.py` closely follow the preserved code. `main.py`, `line_follow.py`, and `green_detection.py` are reconstructed scaffolds because only partial text remained.

## Engineering takeaways
The project integrated computer vision, embedded communication, motion control, mechanical design, and iterative testing into a single autonomous system.
