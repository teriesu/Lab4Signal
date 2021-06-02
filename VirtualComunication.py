import serial

port = "COM4"
baudRate = 9600

com = serial.Serial(port, baudRate)
while True:
    com.write(b'45 * 70 * 40')#.encode('utf-8')
