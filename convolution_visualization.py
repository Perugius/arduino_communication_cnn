import numpy as np
import matplotlib.pyplot as plt

# Define a simple signal and a kernel
signal = np.array([0, 1, 2, 3, 2, 1, 0])
kernel = np.array([1, 0, -1])

# Compute the convolution
convolved = np.convolve(signal, kernel, 'valid')

# Plotting
plt.figure(figsize=(10, 3))
plt.subplot(131)
plt.stem(signal, use_line_collection=True)
plt.title('Signal')
plt.subplot(132)
plt.stem(kernel, use_line_collection=True)
plt.title('Kernel')
plt.subplot(133)
plt.stem(convolved, use_line_collection=True)
plt.title('Convolution')
plt.tight_layout()
plt.show()