from pymavlink import mavutil
import time

class Drone:
    def __init__ (self):
        self.connection = None

    def connect(self):
        # Start a connection listening on a UDP port

        # MIGHT NEED TO CHANGE THIS FOR YOUR OWN DEVICE
        self.connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')

        # Wait for the first heartbeat
        #   This sets the system and component ID of remote system for the link
        self.connection.wait_heartbeat()
        print("Heartbeat from system (system %u component %u)" % (self.connection.target_system, self.connection.target_component))

    def print_ack(self):
        msg = self.connection.recv_match(type='COMMAND_ACK', blocking=True)
        print(msg)
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
        "LAND": 9
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
        mode,                                               
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
    
    