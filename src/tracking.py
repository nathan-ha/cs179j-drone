# Tracks the position of the color red relative to the center of the screen
import time
import cv2
import numpy as np
from picamera2 import Picamera2

CENTER_TOLERANCE = 60
MIN_CONTOUR_AREA = 500
CV_RESULT = "NO TARGET"

def tracking_thread(stopFlag):
    global CV_RESULT
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (640, 480)}
    )
    picam2.configure(config)
    picam2.start()
    print(f"Camera started.")

    while not stopFlag.is_set():
        frame = picam2.capture_array()
        
        height, width = frame.shape[:2]
        frame_center_x = width // 2
        frame_center_y = height // 2
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        
        # Red HSV ranges
        lower_red_1 = np.array([0, 50, 50])
        upper_red_1 = np.array([10, 255, 255])
        lower_red_2 = np.array([170, 50, 50])
        upper_red_2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
        mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
        mask = mask1 | mask2
        
        # Noise reduction
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
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
                    # dy is set to 0 because we are ignoring vertical movement
                    dy = 0 # obj_y - frame_center_y
                    
                    if abs(dx) < CENTER_TOLERANCE and abs(dy) < CENTER_TOLERANCE:
                        direction = "CENTERED"
                    elif abs(dx) > abs(dy):
                        direction = "RIGHT" if dx > 0 else "LEFT"
                    else:
                        direction = "DOWN" if dy > 0 else "UP"
        print(f"Red object direction: {direction}             ", end='\r')
        CV_RESULT = direction
        time.sleep(0.1)
        
    picam2.stop()
    cv2.destroyAllWindows()
    print("Camera stopped.")
