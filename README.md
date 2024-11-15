# Pico Setup Instructions

## Hardware Setup
1. Connect your Raspberry Pi Pico pins:
   - Button to GP0
   - STEP to GP3
   - DIR to GP2
   - EN to GP4

## Software Setup
1. Connect Pico to computer while holding BOOTSEL button
2. Pico will appear as a USB drive
3. Copy `main.py` to the Pico drive
4. Disconnect and reconnect Pico (without BOOTSEL)

## Port Configuration
- Windows: Usually COM3 or COM4
- Linux: Usually /dev/ttyACM0
- Mac: Usually /dev/tty.usbmodem*

## Testing
1. LED should blink when code is running
2. Button press should move conveyor
3. Serial communication should show position updates

## Troubleshooting
- If motor doesn't move, check EN pin connection
- If position tracking is wrong, check STEP_PER_POSITION value
- If button doesn't work, check PULL_UP configuration

## Serial Communication
Motor will respond to these commands:
- "move": Moves to next position
- Response formats:
  - "moving_1": Moving to position 1
  - "moving_2": Moving to position 2
  - "moving_3": Moving to position 3
  - "done": Movement complete
