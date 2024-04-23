import serial
import time
import numpy as np

arduino_port = "COM5"
baud_rate = 115200
ser = serial.Serial(arduino_port, baud_rate, timeout=10, write_timeout=10) # Linux example, change port accordingly

def read_array(ser, num_elements, element_size):
    num_bytes = num_elements * element_size
    data = ser.read(num_bytes)
    return np.frombuffer(data, dtype=np.float32)

def send_array(ser, numpy_array, chunk_size=64):
    bytes_to_send = numpy_array.tobytes()
    for i in range(0, len(bytes_to_send), chunk_size):
        ser.write(bytes_to_send[i:i+chunk_size])
        #time.sleep(0.1)


try:
    while True:
        line = ser.readline().decode().strip()
        print(line)

        if line == "START":
            print("receiving array: ")
            float_array = read_array(ser, 240, 4)
            print(float_array)

        if line == "WAITING":
            print("sending array ")
            send_array(ser, float_array)
            print("sending done")

except KeyboardInterrupt:
    print("Program terminated!")
finally:
    ser.close()  # Ensure serial connection is closed on termination