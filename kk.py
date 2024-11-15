from machine import Pin, Timer
from time import sleep, ticks_ms, ticks_diff

# Initialize pins
buttonA = Pin(0, Pin.IN, Pin.PULL_UP)  # Button to cycle positions
STEP = Pin(3, Pin.OUT)
DIR = Pin(2, Pin.OUT)
EN = Pin(4, Pin.OUT)

# Global variables
last_press_time = 0
debounce_time = 200  # 200ms debounce
button_pressed = False
current_position = 0  # Track current position (0, 1, or 2)
target_steps = 0     # Steps needed to reach target
current_steps = 0    # Current step count

# Constants
STEPS_PER_POSITION = 200  # Adjust based on your needs
TOTAL_POSITIONS = 3
STEP_FREQUENCY = 400  # Steps per second

# Timer for stepping
step_timer = Timer()
running = False  # Flag to track if motor should be stepping

def step_pulse(timer):
    """Generate step pulses and track position"""
    global current_steps, running
    
    if running:
        STEP.toggle()
        if STEP.value() == 0:  # Count only on falling edge
            current_steps += 1
            if current_steps >= target_steps:
                stop_motor()

def stop_motor():
    """Stop the motor movement"""
    global running
    running = False
    STEP.value(0)

def move_to_position(new_position):
    """Calculate steps needed and start movement"""
    global target_steps, current_steps, running
    
    steps_needed = STEPS_PER_POSITION
    current_steps = 0
    target_steps = steps_needed
    running = True
    print(f"Moving to position {new_position + 1}")

def cycle_position(pin):
    """Cycle through the three positions"""
    global last_press_time, current_position, button_pressed
    current_time = ticks_ms()
    
    if pin.value() == 0:  # Button is pressed
        if not button_pressed and ticks_diff(current_time, last_press_time) > debounce_time:
            # Only change position if motor is not currently running
            if not running:
                current_position = (current_position + 1) % TOTAL_POSITIONS
                move_to_position(current_position)
                last_press_time = current_time
            button_pressed = True
    else:  # Button is released
        button_pressed = False

# Set up initial states
EN.value(0)      # Enable motor (active low)
DIR.value(1)     # Set fixed direction

# Configure button interrupt
buttonA.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=cycle_position)

# Start timer for stepping
step_timer.init(freq=STEP_FREQUENCY, mode=Timer.PERIODIC, callback=step_pulse)

try:
    print("Motor control started. Press button to cycle through positions.")
    print("Position 1 is home position")
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    print("\nStopping motor...")
    step_timer.deinit()
    STEP.value(0)
    DIR.value(0)
    EN.value(1)  # Disable motor