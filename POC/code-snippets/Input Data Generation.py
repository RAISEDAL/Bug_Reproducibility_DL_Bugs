import numpy as np

# Generating an Identity Matrix (3x3)
identity_matrix = np.eye(3)

# Generating an Array of Ones (2x4)
ones_array = np.ones((2, 4))

# Generating an Array of Zeros (3x2)
zeros_array = np.zeros((3, 2))

# Generating Random Data with Normal Distribution (2x3)
mean = 0
std_dev = 1
shape = (2, 3)
random_data = np.random.normal(mean, std_dev, shape)

# Generating Random Integers (3x3)
random_integers = np.random.randint(1, 10, (3, 3))

# Generating Random Data from a Uniform Distribution (2x2)
random_uniform_data = np.random.uniform(0, 1, (2, 2))

# Printing the generated data
print("Identity Matrix:\n", identity_matrix)
print("Array of Ones:\n", ones_array)
print("Array of Zeros:\n", zeros_array)
print("Random Data with Normal Distribution:\n", random_data)
print("Random Integers:\n", random_integers)
print("Random Data from Uniform Distribution:\n", random_uniform_data)