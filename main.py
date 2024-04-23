import numpy as np
import serial
import time
import struct

port = "COM5"
baud_rate = 115200


def connect_arduino(port, baud_rate):
    while True:
        try:
            ser = serial.Serial(port, baud_rate, timeout=10, write_timeout=10)
            print("Connected")
            return ser
        except serial.SerialException:
            print("Waiting...")
            time.sleep(0.1)

def read_array(ser, num_bytes):
    data = ser.read(num_bytes)
    return np.frombuffer(data, dtype=np.float32)

def send_array(ser, array):
    data = array.tobytes()
    # send data in chunks of 64 bytes
    for i in range(0, len(data), 64):
        chunk = data[i:i+64]
        ser.write(chunk)
        #print(ser.in_waiting)
        time.sleep(0.05)
        print("writing")

def send_array_elementwise(ser, array):
    ctr = 0
    for fl in array:
        bytes_to_send = struct.pack('f', fl)
        ser.write(bytes_to_send)
        time.sleep(0.01)
        print("writing float: ", ctr)
        ctr += 1

def main():
    # array of inputs for EACH layer
    input_array = []
    # input_array = np.array([], dtype=np.float32)
    # array of outputs from each layer
    output_array = []
    # output_array = np.array([], dtype=np.float32)

    ser = connect_arduino(port, baud_rate)

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(line)
            # Check if arduino is sending data, if yes the arduino sends in the format of ("SENDING "+num_bytes), the array is always appended to output_array
            # when the arduino is sending the first layer I will have to first append it to output_array, then swap the contents to input_array!
            if line.startswith("SENDING "):
                _, num_bytes = line.split()
                num_bytes = int(num_bytes)
                # read the incoming array
                array = read_array(ser, num_bytes)
                output_array.append(array)
                print("RECEIVED DATA")
                print(array)
                print(output_array)
                ser.write("ACK\n".encode())
                time.sleep(0.05)

            # check if arduino is requesting data, if yes the arduino requests a specific channel, which is taken always from input_array
            if line.startswith("REQUESTING "):
                _, needed_channel = line.split()
                needed_channel = int(needed_channel)
                send_array_elementwise(ser, np.array(input_array[needed_channel]))

                print("DATA SENT")
                print(input_array[needed_channel])
                ser.write("ACK\n".encode())
                time.sleep(0.05)

            # check if arduino is moving on to next layer, if yes this means the output_array has to become input_array!
            if line == "SWAP":
                print("SWAP RECEIVED")
                input_array = output_array.copy()
                output_array.clear()
                time.sleep(0.05)

        print("output")
        print(len(output_array))
        print(len(input_array))
        time.sleep(0.5)


if __name__ == "__main__":
    main()