import serial
ser = serial.Serial('YOUR_PORT', 115200)
ser.write(b'move\n')