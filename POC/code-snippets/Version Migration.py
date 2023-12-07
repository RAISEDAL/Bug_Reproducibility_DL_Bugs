# Old Code in Tensorflow v1

import tensorflow as tf

# Define a computation graph
graph = tf.Graph()

with graph.as_default():
    input_data = tf.placeholder(tf.float32, shape=(None, input_size), name="input_data")
    target_data = tf.placeholder(tf.float32, shape=(None, output_size), name="target_data")
    hidden_layer = tf.layers.dense(inputs=input_data, units=64, activation=tf.nn.relu, name="hidden_layer")
    output_layer = tf.layers.dense(inputs=hidden_layer, units=output_size, name="output_layer")

    loss = tf.reduce_mean(tf.square(output_layer - target_data), name="loss")

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
    train_op = optimizer.minimize(loss, name="train_op")

with tf.Session(graph=graph) as sess:
    sess.run(tf.global_variables_initializer())

    for epoch in range(num_epochs):
        _, current_loss = sess.run([train_op, loss], feed_dict={input_data: train_input, target_data: train_target})
        print(f"Epoch {epoch + 1}/{num_epochs}, Loss: {current_loss}")

    predicted_output = sess.run(output_layer, feed_dict={input_data: test_input})




# Updated code in Tensorflow v2
    
import tensorflow as tf
import numpy as np

# Define the model architecture using the Sequential API
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(input_size,), name='hidden_layer'),
    tf.keras.layers.Dense(output_size, name='output_layer')
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01), loss='mean_squared_error')

# Train the model
history = model.fit(train_input, train_target, epochs=num_epochs, batch_size=batch_size, verbose=1)

# Make predictions
predicted_output = model.predict(test_input)

# Print the training history
print("Training history:")
print(history.history)
