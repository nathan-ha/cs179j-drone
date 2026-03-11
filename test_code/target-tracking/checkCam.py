from picamera2 import Picamera2

def camera_connected():
    try:
        picam2 = Picamera2()
        picam2.close()
        return True
    except Exception as e:
        return False

if camera_connected():
    print("Camera is connected")
else:
    print("No camera detected")
