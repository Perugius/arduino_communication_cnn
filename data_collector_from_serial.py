import numpy as np
import serial
import time
import struct

# com port depends on device, Arduno Nano = COM5, Pico W = COM7
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


def send_array_elementwise(ser, array):
    ctr = 0
    for fl in array:
        bytes_to_send = struct.pack('f', fl)
        ser.write(bytes_to_send)
        time.sleep(0.01)
        print("writing float: ", ctr)
        ctr += 1


def main():
    file_path = 'ecg_data/numpy_inputs/'
    #x_data = np.load("ecg_data/numpy_inputs/input_0.npy")
    #x_data = np.load("dfki_data/x_test.npy")#[63].flatten()
    #num_of_inputs = x_data.shape[0]
    #y_data = np.load("dfki_data/y_test.npy")[40]

    result_array = []
    ser = connect_arduino(port, baud_rate)

    for i in range(10):
        filename = 'input_'+str(i)+'.npy'
        x_data = np.load(file_path+filename)
        # iterate over the x_test inputs to send one each i
        current_input = x_data.flatten()
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

    np.save('final_results/arduino_ecg_model_inference_time_00-09.npy', result_array)
    print(result_array)
    time.sleep(1000)

if __name__ == "__main__":
    main()