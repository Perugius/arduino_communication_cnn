import numpy as np

results = np.load("dfki_model_v4_result_array_ARDUINO.npy")
ground_truth = np.load("dfki_data/y_test.npy")
num_of_correct_predictions = 0
i = 0

for arr in results:
    if arr.argmax() == ground_truth[i]:
        num_of_correct_predictions += 1
    i += 1

print(num_of_correct_predictions/len(results))