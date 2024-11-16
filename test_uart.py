# test_uart.py - Upload to Pico
from machine import Pin, UART
import time

# Initialize UART for communication using UART1 (GP8: TX, GP9: RX)
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))

# Initialize onboard LED
led = Pin(25, Pin.OUT)

counter = 0

print("Starting UART test...")

while True:
    # Send a test message every 2 seconds
    message = f"Pico test message {counter}\n"
    uart.write(message.encode())
    print(f"Sent: {message.strip()}")
    
    # Blink LED to show we're sending
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    
    # Check for incoming messages
    if uart.any():
        try:
            received = uart.read().decode().strip()
            print(f"Received: {received}")
            
            # Blink LED twice for received message
            for _ in range(2):
                led.value(1)
                time.sleep(0.1)
                led.value(0)
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Error reading: {e}")
    
    counter += 1
    time.sleep(2)  # Wait 2 seconds before next message