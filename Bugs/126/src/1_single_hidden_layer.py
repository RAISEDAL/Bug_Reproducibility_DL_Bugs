import os
import numpy as np
from pandas.io.parsers import read_csv
from sklearn.utils import shuffle

dirname = os.path.dirname(os.path.realpath(__file__))
#place the .csv files one level up and within data/kaggle-facial-keypoint-detection folder.
FTRAIN = os.path.join(dirname, '../data/training.csv')
FTEST = os.path.join(dirname, '../data/test.csv')

def load(test=False, cols=None):
    """Loads data from FTEST if *test* is True, otherwise from FTRAIN.
    Pass a list of *cols* if you're only interested in a subset of the
    target columns.
    """
    fname = FTEST if test else FTRAIN
    df = read_csv(os.path.expanduser(fname))  # load pandas dataframe

    # The Image column has pixel values separated by space; convert
    # the values to numpy arrays:
    df['Image'] = df['Image'].apply(lambda im: np.fromstring(im, sep=' '))

    if cols:  # get a subset of columns
        df = df[list(cols) + ['Image']]

    print(df.count())  # prints the number of values for each column
    df = df.dropna()  # drop all rows that have missing values in them

    X = np.vstack(df['Image'].values) / 255.  # scale pixel values to [0, 1]
    X = X.astype(np.float32)

    if not test:  # only FTRAIN has any target columns
        y = df[df.columns[:-1]].values
        y = (y - 48) / 48  # scale target coordinates to [-1, 1]
        X, y = shuffle(X, y, random_state=42)  # shuffle train data
        y = y.astype(np.float32)
    else:
        y = None

    return X, y




X, y = load()
print("X.shape == {}; X.min == {:.3f}; X.max == {:.3f}".format(
    X.shape, X.min(), X.max()))
print("y.shape == {}; y.min == {:.3f}; y.max == {:.3f}".format(
    y.shape, y.min(), y.max()))

# Create the keras model
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

# import keras.backend as K

# def get_categorical_accuracy_keras(y_true, y_pred):
#   return K.mean(K.equal(K.argmax(y_true, axis=1), K.argmax(y_pred, axis=1)))

# Version - Single Hidden Layer
model = Sequential()
model.add(Dense(50, input_shape=(9216,))) # Input Batches of 96x96 input pixels per batch
model.add(Dense(100))
model.add(Dense(30)) # 30 to represent 30 facial keypoints.

#   Compile the model.  Minimize mean squared error  Maximize for accuracy
model.compile(Adam(lr=0.1), 'mean_squared_error') #, metrics=['accuracy'])

#   Fit the model with the data from make_blobs.  Make 100 cycles through the data.
#   Set verbose to 0 to supress progress messages 
model.fit(X, y, epochs=100, verbose=1)
#   Get loss and accuracy on test data
eval_result = model.evaluate(X, y)
#   Print test accuracy
print("\n\nTest loss:", eval_result)
# Save fine tuned model
model.save('1_single_hidden_layer.h5')

# ///////// Added By @Mehdi
import json
file = open(file="buggy/result.json", mode="w")  
model_loss = np.float64(eval_result)
res = {"loss" : model_loss}
json.dump(res, file)
file.close()