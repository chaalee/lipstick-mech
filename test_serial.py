# test_serial.py - Run on your computer
import serial
import time

def test_serial_connection():
    try:
        # Connect to the serial port
        ser = serial.Serial(
            port='/dev/tty.usbserial-A104VDBO',  # Your serial port
            baudrate=115200,
            timeout=1
        )
        print("Serial port opened successfully")
        
        # Send and receive loop
        counter = 0
        while True:
            try:
                # Check for incoming messages
                if ser.in_waiting:
                    message = ser.readline().decode().strip()
                    print(f"Received from Pico: {message}")
                
                # Send test message every 3 seconds
                if counter % 3 == 0:
                    test_message = f"Server test {counter}\n"
                    ser.write(test_message.encode())
                    print(f"Sent to Pico: {test_message.strip()}")
                
                counter += 1
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\nTest stopped by user")
                break
            except Exception as e:
                print(f"Error during communication: {e}")
                break
                
    except Exception as e:
        print(f"Error opening serial port: {e}")
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    print("Starting serial communication test...")
    test_serial_connection()