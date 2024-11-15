# main.py for Pico
from machine import Pin, Timer, UART
from time import sleep, ticks_ms, ticks_diff

# Initialize UART for communication
uart = UART(0, baudrate=115200)

# Initialize pins
STEP = Pin(3, Pin.OUT)
DIR = Pin(2, Pin.OUT)
EN = Pin(4, Pin.OUT)
LED = Pin(25, Pin.OUT)  # Onboard LED for status

# Global variables
current_position = 0
target_steps = 0
current_steps = 0
sequence_running = False
current_sequence_position = 0

# Constants
STEPS_PER_POSITION = 400  # Increased steps for visible movement
TOTAL_POSITIONS = 3
STEP_FREQUENCY = 1000  # Increased frequency for faster movement
DELAY_BETWEEN_MOVES = 2

# Timer for stepping
step_timer = Timer()
running = False

def blink_led(times=1):
    """Blink LED for visual feedback"""
    for _ in range(times):
        LED.toggle()
        sleep(0.1)
        LED.toggle()
        sleep(0.1)

def step_pulse(timer):
    """Generate step pulses and track position"""
    global current_steps, running, sequence_running, current_sequence_position
    
    if running:
        STEP.toggle()
        LED.value(STEP.value())  # LED mirrors STEP signal
        
        if STEP.value() == 0:  # Count only on falling edge
            current_steps += 1
            if current_steps >= target_steps:
                stop_motor()
                print("Position reached")
                uart.write('done\n'.encode())
                blink_led(2)  # Visual feedback for position reached
                
                if sequence_running:
                    current_sequence_position += 1
                    if current_sequence_position < TOTAL_POSITIONS:
                        sleep(DELAY_BETWEEN_MOVES)
                        move_to_position(current_sequence_position)
                    else:
                        sequence_running = False
                        current_sequence_position = 0
                        uart.write('sequence_complete\n'.encode())
                        print("Sequence complete")
                        blink_led(3)  # Visual feedback for sequence complete

def stop_motor():
    """Stop the motor movement"""
    global running
    running = False
    STEP.value(0)
    print("Motor stopped")

def move_to_position(new_position):
    """Calculate steps needed and start movement"""
    global target_steps, current_steps, running, current_position
    
    print(f"Moving to position {new_position + 1}")
    steps_needed = STEPS_PER_POSITION
    current_steps = 0
    target_steps = steps_needed
    running = True
    current_position = new_position
    
    # Set direction based on position
    DIR.value(1)  # Set direction (adjust if needed)
    
    uart.write(f'moving_{new_position + 1}\n'.encode())
    blink_led(1)  # Visual feedback for movement start

def start_automatic_sequence():
    """Start the automatic sequence through all positions"""
    global sequence_running, current_sequence_position
    
    if not running and not sequence_running:
        print("Starting automatic sequence")
        sequence_running = True
        current_sequence_position = 0
        move_to_position(0)
        uart.write('sequence_started\n'.encode())
        blink_led(2)

# Initial setup
print("Initializing motor control...")
EN.value(0)      # Enable motor (active low)
DIR.value(1)     # Set initial direction
LED.value(0)     # Start with LED off

# Test motor driver
print("Testing motor driver...")
EN.value(1)      # Disable briefly
sleep(0.1)
EN.value(0)      # Re-enable
blink_led(3)     # Startup indicator

# Start timer for stepping
step_timer.init(freq=STEP_FREQUENCY, mode=Timer.PERIODIC, callback=step_pulse)

print("Motor control started. Ready for commands.")
print("EN pin:", EN.value())
print("DIR pin:", DIR.value())
print("STEP initial state:", STEP.value())

# Main loop
while True:
    if uart.any():
        try:
            command = uart.read().decode().strip()
            print(f"Received command: {command}")
            
            if command == "move":
                print("Starting movement sequence")
                start_automatic_sequence()
                blink_led(1)
            
        except Exception as e:
            print(f"Error processing command: {e}")
    
    sleep(0.01)