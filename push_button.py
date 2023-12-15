import serial

# Replace 'COM3' with the appropriate serial port where your Arduino is connected
ser = serial.Serial('COM5', 9600)

while True:
    arduino_data = ser.readline().decode().strip()  # Read and decode the data from Arduino
    if arduino_data == "1":
        print("Button pressed: 1 received from Arduino")
    if arduino_data == "0":
        print("ok")
        # Add your code to perform actions when the button is pressed
