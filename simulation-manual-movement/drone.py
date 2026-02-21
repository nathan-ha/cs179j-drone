from pymavlink import mavutil
import time

class Drone:
    def __init__ (self):
        self.connection = None

    def connect(self):
        # Start a connection listening on a UDP port

        # MIGHT NEED TO CHANGE THIS FOR YOUR OWN DEVICE
        #self.connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
        self.connection = mavutil.mavlink_connection('COM9', baud=115200) #for serial (laptop ports)
        self.connection.mav.param_set_send(
        self.connection.target_system,
        self.connection.target_component,
        b'GPS_TYPE',
        0,  # 0 = None
        mavutil.mavlink.MAV_PARAM_TYPE_INT32
        )

        # Wait for the first heartbeat
        #   This sets the system and component ID of remote system for the link
        self.connection.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.connection.target_system, self.connection.target_component))

    def print_ack(self):
        msg = self.connection.recv_match(type='COMMAND_ACK', blocking=True)
        print(msg)
        # msg = self.connection.recv_match(type='STATUSTEXT', blocking=True)
        # print(msg)
        return msg

    def arm(self):
        print("ARM")

        self.connection.mav.command_long_send(self.connection.target_system, 
        self.connection.target_component, 
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
        0, 
        1, 
        0, 
        0, 0, 0, 0, 0)
        
        self.print_ack()  

    def dearm(self):
        print("DEARM")

        self.connection.mav.command_long_send(self.connection.target_system, 
        self.connection.target_component, 
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 
        0, 
        0, 
        0, 
        0, 0, 0, 0, 0)
        
        self.print_ack()  

    def set_mode(self, mode):
        modes = {
        "STABILIZE": 0,
        "ACRO": 1,
        "ALT_HOLD": 2,
        "AUTO": 3,
        "GUIDED": 4,
        "LOITER": 5,
        "RTL": 6,
        "CIRCLE": 7,
        "LAND": 9,
        "NOGPS": 20
        }

        # Bidirectional 
        reverse_modes = {v: k for k, v in modes.items()}
        if isinstance(mode, str):
            print("MODE:", mode)
            mode = modes[mode]
        else:
            print("MODE:", reverse_modes[mode])
        

        self.connection.mav.command_long_send(
        self.connection.target_system,
        self.connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode,                            #changed from mode -> 20 (for no gps)                    
        0, 0, 0, 0, 0
        )
        self.print_ack()  

    # | Mode             | ID |
    # | ---------------- | -- |
    # | **STABILIZE**    | 0  |
    # | **ACRO**         | 1  |
    # | **ALT_HOLD**     | 2  |
    # | **AUTO**         | 3  |
    # | **GUIDED**       | 4  |
    # | **LOITER**       | 5  |
    # | **RTL**          | 6  |
    # | **CIRCLE**       | 7  |
    # | **LAND**         | 9  |
    # NOGPS 20

    # The mode either the ID or the string
    def takeoff(self, altitude):
        print("TAKEOFF")

        self.connection.mav.command_long_send(
            self.connection.target_system, 
            self.connection.target_component, 
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 
            0, 
            0, 0, 0, 0, 
            0, 0, 
            float(altitude))


        # Wait for drone to reach altitude
        result = self.print_ack()

        if result.result == 0:
            while True:
                msg = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
                alt_m = msg.relative_alt / 1000.0 
                if alt_m >= altitude * 0.8:       
                    print(f"Reached {altitude} m")
                    break
                time.sleep(0.1)

    def move(self, x, y, z):
        self.connection.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            0,                                   
            self.connection.target_system,
            self.connection.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED, 
            int(0b110111111000),
            x, y, z,     # x, y, z COORDINATES
            0, 0, 0,       # x, y, z VELOCITY
            0, 0, 0,    
            0, 0  
        ))
    # Using Pymavlink

# Send text message to GCS
# master.mav.statustext_send(
#     mavutil.mavlink.MAV_SEVERITY_INFO,
#     "Hello from MAVLink!".encode('utf-8')
#)

    def printMav(self):
        self.connection.mav.statustext_send(
            mavutil.mavlink.MAV_SEVERITY_INFO,
            "Hello from MAVLink!".encode('utf-8')

        )
    def test(self):
        start_time = time.time()
        duration = 3  # seconds to lift off
        while time.time() - start_time < duration:
            self.connection.mav.set_attitude_target_send(
            1000,#int(time.time()*1000),  # time_boot_ms
            self.connection.target_system,
            self.connection.target_component,
            0b00000111,              # ignore body rates
            [1, 0, 0, 0],            # level orientation (quaternion)
            0, 0, 0,                 # roll_rate, pitch_rate, yaw_rate
            0.6                    # throttle (0–1)
            )
        #self.print_ack()
        time.sleep(0.1)
    
    def test2(self):
        start_time = time.time()
        duration = 3  # seconds to lift off
        while time.time() - start_time < duration:
            self.connection.mav.set_attitude_target_send(
            1000,#int(time.time()*1000),  # time_boot_ms
            self.connection.target_system,
            self.connection.target_component,
            0b00000111,              # ignore body rates
            [1, 0, 0, 0],            # level orientation (quaternion)
            0, 0, 0,                 # roll_rate, pitch_rate, yaw_rate
            0.3                    # throttle (0–1)
            )
        #self.print_ack()
        time.sleep(0.1)