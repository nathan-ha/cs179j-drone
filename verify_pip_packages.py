packages = {
    "opencv": "cv2",
    "rpicamera2": "picamera2",
    "pymavlink": "pymavlink"
}

for name, module in packages.items():
    try:
        __import__(module)
        print(f"{name} is installed")
    except ImportError:
        print(f"{name} is NOT installed")




