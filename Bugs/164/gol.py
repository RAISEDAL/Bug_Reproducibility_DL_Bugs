"""
Training neural network to play Conway's Game of Life
"""

import numpy as np
import tensorflow as tf


def generate_field(shape, alive_prob=0.5):
    return (np.random.rand(*shape) < alive_prob).astype(np.int32)


def update_field(field, hw_axis=(1, 2)):
    """
    Calculates next state for the cell field according to the rules.

    Params:
    -------

    field: ndarray, usually of shape (N, H, W, 1), N-num of samples, H-height, W-width
    hw_axis: tuple with the order of height and width dimension in field shape.

    Returns:
    --------

    ndarray: field of the same shape for the next state.
    """
    h_ax, w_ax = hw_axis

    neighbours = np.zeros(field.shape, dtype=np.int32)
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if not (dx or dy):
                continue
            neighbours += np.roll(np.roll(field, dx, w_ax), dy, h_ax)

    return np.logical_or(
        neighbours==3,
        np.logical_and(field, neighbours==2)
    ).astype(np.int32)


def pad_field(field):
    """
    Pads H and W dimensions to emulate cyclic nature of cell field.

    Params:
    -------

    field: ndarray (N, H, W, 1), N-num of samples, H-height, W-width

    Returns:
    --------

    ndarray (N, H+2, W+2, 1)
    """
    return np.pad(field, ((0,0), (1,1), (1,1), (0,0)), mode='wrap')


def generate_dataset(num_samples, height, width, alive_prob=0.5):
    """
    Generates dataset with shape (num_samples, height, width, 1) where each
    cell is alive with alive_prob.

    Returns:
    --------

    tuple (X, y)
    X: ndarray (N, H, W, 1) field states
    y: ndarray (N, H, W, 1) corresponding next states
    """
    shape = (num_samples, height, width, 1)
    X = generate_field(shape, alive_prob)
    y = update_field(X)
    return X, y


def life_nn(
        height,
        width,
        num_filters=10,
        num_channels=20,
        loss='binary_crossentropy',
        optimizer='adam'
    ):
    """
    Create CNN model for the Game of Life.

    In game's rules next state of a cell depends only on its neighbours.

    Thats why (3,3) conv filters is a reasonable choice for the first layer.
    For this layer 'valid' padding is used to shrink shape to the original size
    of the field.

    Then (1,1) convolution layer with num_channels filters is used.

    And finally another (1,1) convolution with just 1 output channel.

    (N, H+2, W+2, 1)
           |
        conv1 (3,3)
           |
    (N, H, W, num_filters)
           |
        conv2 (1,1)
           |
    (N, H, W, num_channels)
           |
        conv3 (1,1)
           |
    (N, H, W, 1)
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(
            num_filters,
            kernel_size=(3, 3),
            strides=(1, 1),
            padding="valid",
            use_bias=True,
            activation='relu',
            input_shape=(height+2, width+2) + (1,)
        ),
        tf.keras.layers.Conv2D(
            num_channels,
            kernel_size=(1, 1),
            strides=(1, 1),
            padding="same",
            use_bias=True,
            activation='relu'
        ),
        tf.keras.layers.Conv2D(
            1,
            kernel_size=(1, 1),
            strides=(1, 1),
            padding="same",
            use_bias=True,
            activation='sigmoid'
        )
    ])
    model.compile(loss=loss, optimizer=optimizer, metrics=['accuracy'])
    return model


def train(model, X_train, y_train, X_val, y_val, batch_size=64, epochs=1):
    """
    Trains NN model on train and validation set.
    Wrap pads input fields to prevent errors on the border.
    """
    X_train_padded = pad_field(X_train)
    X_val_padded = pad_field(X_val)
    model.fit(X_train_padded, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(X_val_padded, y_val)
    )


def evaluate(model, X_test, y_test, batch_size=64):
    """
    Evaluates model's loss and accuracy on the test set.
    Wrap pads input fields before the evaluation.
    """
    X_test_padded = pad_field(X_test)
    return model.evaluate(
        X_test_padded,
        y_test,
        batch_size=batch_size,
        verbose=False
    )


def evaluate_prob_grid(model):
    """
    Generates test dataset for different alive probabilities
    and checks model performance.
    """
    total_loss = 0
    total_acc = 0
    counter = 0
    shape = model.input_shape
    height, width = shape[1] - 2, shape[2] - 2
    for alive_prob in np.linspace(0.1, 0.9, 9): 
        X_test, y_test = generate_dataset(1000, height, width, alive_prob)
        loss, acc = evaluate(model, X_test, y_test)
        counter = counter + 1
        total_acc = total_acc + acc
        total_loss = total_loss + loss
        print('P_alive={:.1f} Loss:{:.2f} Acc:{:.2f}'.format(alive_prob, loss, acc))

    # ///////// Added By @Mehdi
    import json
    file = open(file="result.json", mode="w")  
    model_loss = np.float64(total_loss/counter)
    res = {"loss" : model_loss}
    json.dump(res, file)
    file.close()
    # /////////////////////


def print_evolution(height, width, alive_prob=0.5, epochs=20):
    """
    Visualize field evolution for debugging purposes.
    """
    import time
    field = generate_field((height, width))

    def print_field(field):
        for row in field:
            print(''.join('X' if x else '.' for x in row))

    for epoch in range(epochs):
        print('Epoch:', epoch)
        print_field(field)
        print()
        field = update_field(field, hw_axis=(0,1))
        time.sleep(0.3)


if __name__ == '__main__':
    import sys
    height = int(sys.argv[1])
    width = int(sys.argv[2])

    print('Building model:')
    model = life_nn(height, width)
    model.summary()
    print()

    num_train_samples = 15000
    num_val_samples = 3000
    X_train, y_train = generate_dataset(num_train_samples, height, width)
    X_val, y_val = generate_dataset(num_val_samples, height, width)

    print('Training model:')
    train(model, X_train, y_train, X_val, y_val, epochs=5)
    print()

    print('Evaluating model:')
    evaluate_prob_grid(model)
