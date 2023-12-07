import numpy as np

random_uniform_data = np.random.uniform(0, 1, (2, 2))
print (random_uniform_data.shape)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),  # Hidden layer with ReLU activation
    keras.layers.Dense(64, activation='relu'),   # Additional hidden layer
    keras.layers.Dense(10, activation='softmax')
])
print (model.summary())