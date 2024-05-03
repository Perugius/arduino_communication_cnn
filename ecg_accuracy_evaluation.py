import numpy as np
import os

result_path = 'ecg_data/pico_result_data/'
gt_path = 'ecg_data/HALF2_4812_gt/'
ground_truths = []
complete_result = []
threshold = 0.5

testing = np.load("ecg_data/complete_results_raspi.npy")

# format results in case they are split into multiple files
# for i in range(10):
#     arr = np.load(result_path + f'pico_ecg_model_result_array_{i}0-{i}9.npy')[:, 0]
#     complete_result.append(arr)
#
# complete_result_array = np.concatenate(complete_result, axis=0)
# np.save('ecg_data/complete_results_pico.npy', complete_result_array)
# print(complete_result_array)


# format ground truths from 100 text files to a single numpy array
# Loop through the file names
# for i in range(100):
#     file_path = os.path.join(gt_path, f'{i:08d}.txt')  # Formats the filename
#
#     # Open and read the file
#     with open(file_path, 'r') as file:
#         value = file.read().strip()  # Read the content and strip any extra whitespace/newlines
#         ground_truths.append(int(value))  # Convert the string to an integer and append to the list
#
# # Convert the list of ground truths to a NumPy array
# gt_array = np.array(ground_truths)
# np.save('ecg_data/ground_truths.npy', gt_array)


ground_truths = np.load("ecg_data/ground_truths.npy")
predictions = (testing>= threshold).astype(int)
correct_predictions = (predictions == ground_truths)
accuracy = correct_predictions.mean()
print(f'Accuracy: {accuracy:.2f}')
