# main.py for Pico
from machine import Pin, UART
import time

# Initialize UART for communication
uart = UART(0, baudrate=115200)

# Initialize pins
STEP = Pin(3, Pin.OUT)
DIR = Pin(2, Pin.OUT)
EN = Pin(4, Pin.OUT)
LED = Pin(25, Pin.OUT)  # Onboard LED

# Motor control variables
current_position = 0
is_moving = False

def move_motor(steps=400):
    """Basic motor movement function"""
    global is_moving
    
    try:
        is_moving = True
        print("Moving motor...")
        LED.value(1)  # Turn on LED during movement
        
        for _ in range(steps):
            STEP.value(1)
            time.sleep(0.001)
            STEP.value(0)
            time.sleep(0.001)
            
        LED.value(0)  # Turn off LED
        print("Movement complete")
        uart.write('done\n'.encode())
        
    except Exception as e:
        print(f"Error moving motor: {e}")
    finally:
        is_moving = False

# Initialize motor
print("Initializing motor control...")
EN.value(0)  # Enable motor
DIR.value(1)  # Set direction

# Blink LED to show initialization complete
for _ in range(3):
    LED.value(1)
    time.sleep(0.1)
    LED.value(0)
    time.sleep(0.1)

print("Motor control started. Ready for commands.")

# Main loop
while True:
    if uart.any():
        try:
            command = uart.read().decode().strip()
            print(f"Received command: {command}")
            
            if command == "move" and not is_moving:
                uart.write('moving_1\n'.encode())
                move_motor()
                
        except Exception as e:
            print(f"Error processing command: {e}")
            
    time.sleep(0.01)
