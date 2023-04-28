import serial
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM6'
ser
ser.open()
msg = ser.readline()
msg2 = str(msg,'utf-8')
print(msg2)