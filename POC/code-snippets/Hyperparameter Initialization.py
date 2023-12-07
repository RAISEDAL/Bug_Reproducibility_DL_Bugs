import random
import numpy as np

# Define hyperparameter search space
batch_sizes = [16, 32, 64, 128]
num_epochs = random.randint(10, 100)  # Random number of epochs between 10 and 100
learning_rate = 10 ** random.uniform(-5, -2)  # Random learning rate in the range [1e-5, 1e-2]

# Randomly select hyperparameters
batch_size = random.choice(batch_sizes)

# Print randomly generated hyperparameters
print("Randomly Generated Hyperparameters:")
print("Batch Size:", batch_size)
print("Number of Epochs:", num_epochs)
print("Learning Rate:", learning_rate)