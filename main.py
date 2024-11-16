# main.py for Pico
from machine import Pin, UART
import time

# Initialize UART for communication using UART1 (GP8: TX, GP9: RX)
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

# Initialize pins
STEP = Pin(3, Pin.OUT)
DIR = Pin(2, Pin.OUT)
EN = Pin(4, Pin.OUT)
LED = Pin(25, Pin.OUT)

# Constants
STEPS_PER_POSITION = 200
TOTAL_POSITIONS = 3
DELAY_BETWEEN_POSITIONS = 2

# Variables
current_position = 0
is_moving = False

def move_motor(steps=200, direction=1):
    """Move motor for specified steps in given direction"""
    global is_moving
    
    try:
        is_moving = True
        LED.value(1)
        
        # Set direction (1 forward, 0 backward)
        DIR.value(direction)
        
        for _ in range(steps):
            STEP.value(1)
            time.sleep(0.001)
            STEP.value(0)
            time.sleep(0.001)
            
        LED.value(0)
        
    except Exception as e:
        print(f"Error moving motor: {e}")
    finally:
        is_moving = False

def return_to_home():
    """Return conveyor to home position"""
    global current_position
    
    if current_position == 0:
        uart.write('already_home\n'.encode())
        return
        
    try:
        print("Returning to home position")
        uart.write('homing\n'.encode())
        
        # Calculate steps needed to return home
        steps_to_home = current_position * STEPS_PER_POSITION
        
        # Move backward to home
        move_motor(steps_to_home, direction=0)
        
        current_position = 0
        uart.write('home_reached\n'.encode())
        print("Home position reached")
        
    except Exception as e:
        print(f"Error returning home: {e}")
        uart.write('error\n'.encode())

def move_sequence():
    """Execute complete three-position movement sequence"""
    global current_position
    
    try:
        # First position
        print("Moving to position 1")
        uart.write('moving_1\n'.encode())
        move_motor(STEPS_PER_POSITION, direction=1)
        current_position = 1
        uart.write('reached_1\n'.encode())
        time.sleep(DELAY_BETWEEN_POSITIONS)
        
        # Second position
        print("Moving to position 2")
        uart.write('moving_2\n'.encode())
        move_motor(STEPS_PER_POSITION, direction=1)
        current_position = 2
        uart.write('reached_2\n'.encode())
        time.sleep(DELAY_BETWEEN_POSITIONS)
        
        # Third position
        print("Moving to position 3")
        uart.write('moving_3\n'.encode())
        move_motor(STEPS_PER_POSITION, direction=1)
        current_position = 3
        uart.write('reached_3\n'.encode())
        
        # Sequence complete
        print("Sequence complete")
        uart.write('sequence_complete\n'.encode())
        
    except Exception as e:
        print(f"Error in sequence: {e}")
        uart.write('error\n'.encode())

# Initialize
print("Initializing motor control...")
EN.value(0)
DIR.value(1)

# Startup indicator
for _ in range(3):
    LED.value(1)
    time.sleep(0.1)
    LED.value(0)
    time.sleep(0.1)

print("Ready for commands")

# Main loop
while True:
    if uart.any():
        try:
            command = uart.read().decode().strip()
            print(f"Received command: {command}")
            
            if command == "move" and not is_moving:
                move_sequence()
            elif command == "home" and not is_moving:
                return_to_home()
                
        except Exception as e:
            print(f"Error processing command: {e}")
            
    time.sleep(0.01)
