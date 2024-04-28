import numpy as np
import os

directory_path = 'ecg_data/HALF2_4812_preprocessed_input/'
#
# for i in range(100):
#     filename = f"{i:08}.txt"
#     file_path = os.path.join(directory_path, filename)
#     print(file_path)
#     with open(file_path, 'r') as file:
#         array_list = [float(line.strip()) for line in file]
#
#     numpy_array = np.array(array_list, dtype=np.float32)
#     np.save("ecg_data/numpy_inputs/input_"+str(i)+".npy", numpy_array)
#
# for i in range(100):
#     filename = "ecg_data/numpy_inputs/input_"+str(i)+".npy"
#     arr = np.load(filename)
#     print(arr)

numpy_array = np.load('ecg_data/numpy_inputs/input_1.npy')
f = open("ecg_data/cpp_inputs/input_1.h", 'w+')

f.write("#ifndef INPUT_H\n#define INPUT_H\n\n")
f.write("const int first_input_length = "+str(len(numpy_array)/2)+';\n')
f.write("const int first_num_of_channels = "+"2"+';\n')
f.write("const float test_data[] = { \n")

for d in numpy_array:
    f.write(str(d))
    f.write(', ')
f.write('};\n\n')
f.write('#endif // INPUT_H')
f.close()
