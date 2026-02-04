import cv2
import numpy as np
from picamera2 import Picamera2
import argparse

print('\n\n Available flags: --hide (default), --show, --help \n\n') 
# ----------------------------
# Parse command-line arguments
# ----------------------------
parser = argparse.ArgumentParser(description='Track red objects using Raspberry Pi camera')
parser.add_argument('--show', action='store_true', 
                    help='Show camera window (requires display/X11)')
parser.add_argument('--hide', dest='show_window', action='store_false',
                    help='Run in headless mode (default)')
parser.set_defaults(show_window=False)

args = parser.parse_args()

# ----------------------------
# Configuration
# ----------------------------
CENTER_TOLERANCE = 40
MIN_CONTOUR_AREA = 500
SHOW_WINDOW = args.show_window

# ----------------------------
# Initialize camera
# ----------------------------
picam2 = Picamera2()

# Configure camera for OpenCV (BGR format)
config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(config)
picam2.start()

print(f"Camera started. Window display: {'ON' if SHOW_WINDOW else 'OFF'}")
print("Press Ctrl+C to quit.")

# ----------------------------
# Main loop
# ----------------------------
try:
    while True:
        # Capture frame from picamera2
        frame = picam2.capture_array()
        
        # Convert RGB to BGR for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
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
            # short sleep to avoid 100% cpu
            cv2.waitKey(1)
        
        print(direction)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    # ----------------------------
    # Cleanup
    # ----------------------------
    picam2.stop()
    cv2.destroyAllWindows()
    print("Camera stopped.")
