import cv2
import numpy as np

# ----------------------------
# Configuration
# ----------------------------
CAMERA_INDEX = 0
CENTER_TOLERANCE = 40
MIN_CONTOUR_AREA = 500

SHOW_WINDOW = True   # ← set to True to enable OpenCV window

# ----------------------------
# Initialize camera
# ----------------------------
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    raise RuntimeError("Could not open camera")

# ----------------------------
# Main loop
# ----------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    frame_center_x = width // 2
    frame_center_y = height // 2

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red HSV ranges
    lower_red_1 = np.array([0, 120, 70])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 120, 70])
    upper_red_2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = mask1 | mask2

    # Noise reduction
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    direction = "NO TARGET"

    if contours:
        largest = max(contours, key=cv2.contourArea)

        if cv2.contourArea(largest) > MIN_CONTOUR_AREA:
            M = cv2.moments(largest)

            if M["m00"] != 0:
                obj_x = int(M["m10"] / M["m00"])
                obj_y = int(M["m01"] / M["m00"])

                dx = obj_x - frame_center_x
                dy = obj_y - frame_center_y

                if abs(dx) < CENTER_TOLERANCE and abs(dy) < CENTER_TOLERANCE:
                    direction = "CENTERED"
                elif abs(dx) > abs(dy):
                    direction = "RIGHT" if dx > 0 else "LEFT"
                else:
                    direction = "DOWN" if dy > 0 else "UP"

                if SHOW_WINDOW:
                    cv2.circle(frame, (obj_x, obj_y), 6, (0, 255, 0), -1)

    if SHOW_WINDOW:
        cv2.circle(frame, (frame_center_x, frame_center_y), 4, (255, 0, 0), -1)
        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Small sleep avoids 100% CPU in headless mode
        cv2.waitKey(1)

    print(direction)

# ----------------------------
# Cleanup
# ----------------------------
cap.release()
cv2.destroyAllWindows()
