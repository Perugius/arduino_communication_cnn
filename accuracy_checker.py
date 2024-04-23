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
        time.sleep(0.01)
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
    x_data = np.load("dfki_data/x_test.npy")#[63].flatten()
    num_of_inputs = x_data.shape[0]
    #y_data = np.load("dfki_data/y_test.npy")[40]

    result_array = []
    ser = connect_arduino(port, baud_rate)

    for i in range(num_of_inputs):
        # iterate over the x_test inputs to send one each i
        current_input = x_data[i].flatten()
        print(current_input)
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                print(line)

                if line.startswith("SENDING "):
                    _, num_bytes = line.split()
                    num_bytes = int(num_bytes)
                    # read the incoming array
                    output_array = read_array(ser, num_bytes)
                    print("RECEIVED DATA")
                    print(output_array)
                    ser.write("ACK\n".encode())
                    time.sleep(0.05)
                    result_array.append(output_array)
                    # when inference result is received break out of while loop and move on to next i
                    break

                if line.startswith("REQUESTING "):
                    send_array_elementwise(ser, np.array(current_input).astype(np.float32))
                    print("DATA SENT")
                    print(current_input)
                    ser.write("ACK\n".encode())
                    time.sleep(0.05)

    np.save('dfki_model_v4_result_array.npy', result_array)
    print(result_array)
    time.sleep(1000)

if __name__ == "__main__":
    main()