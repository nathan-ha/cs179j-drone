#!/usr/bin/env python3
from pymavlink import mavutil
import time

# 1. Create connection (adjust IP/port as needed)
master = mavutil.mavlink_connection('udp:127.0.0.1:14550') #for qgc
#master = mavutil.mavlink_connection('COM9', baud=115200) #for serial (laptop ports)

# 2. Wait for heartbeat
print("Waiting for heartbeat...")
master.wait_heartbeat()
print("Connected!")

# 3. Send a message to QGroundControl
def send_message(text, severity=6):
    """
    Send text message to QGroundControl
    
    Severity:
    2 = Critical (RED)
    3 = Error (RED)
    4 = Warning (YELLOW)
    5 = Notice (WHITE)
    6 = Info (WHITE)
    """
    master.mav.statustext_send(
        severity=severity,
        text=text[:50].encode('utf-8')
    )

# ============================================
# EXAMPLES
# ============================================

# Example 1: Simple message
send_message("Hello from Python!")
time.sleep(1)

# Example 2: Warning message (yellow)
send_message("Battery low!", severity=4)
time.sleep(1)

# Example 3: Critical message (red)
send_message("GPS lost!", severity=2)
time.sleep(1)

# Example 4: Multiple messages
messages = [
    ("System starting...", 6),
    ("Sensors initialized", 6),
    ("GPS acquired", 5),
    ("Ready to fly", 6)
]

for msg, sev in messages:
    send_message(msg, sev)
    time.sleep(2)

print("Done! Check QGroundControl for messages")

# ============================================
# COMMON CONNECTION STRINGS
# ============================================
"""
UDP (most common):
- 'udp:127.0.0.1:14550'  (local)
- 'udp:192.168.1.100:14550'  (remote)

Serial:
- '/dev/ttyUSB0:57600'  (Linux)
- 'COM3:57600'  (Windows)
- '/dev/tty.usbserial:57600'  (Mac)

TCP:
- 'tcp:127.0.0.1:5760'
"""
