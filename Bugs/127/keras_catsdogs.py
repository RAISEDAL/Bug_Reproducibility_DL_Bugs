#!/usr/bin/env python3
#coding=UTF-8

'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from scipy.misc import imread, imsave, imresize
import glob
import numpy as np

batch_size = 200
num_classes = 2
epochs = 10

# input image dimensions
img_rows, img_cols = 64, 64
img_channels = 3

# load my custom data
folder = "catsdogsdataset64"
dogs_folder = "dogs64"
cats_folder = "cats64"


filelist = glob.glob(folder + '/' + dogs_folder + '/*')
train_dogs = np.array([np.array(imread(filename).flatten()) for filename in filelist])
# print(f"train My print{train_dogs.shape}")
train_dogs_y = np.zeros((len(filelist),1))
filelist = glob.glob(folder + '/' + dogs_folder + '_test/*')
test_dogs = np.array([np.array(imread(filename).flatten()) for filename in filelist])
# print(f"train My print{test_dogs.shape}")
test_dogs_y = np.zeros((len(filelist),1))

filelist = glob.glob(folder + '/' + cats_folder + '/*')
train_cats = np.array([np.array(imread(filename).flatten()) for filename in filelist])
train_cats_y = np.ones((len(filelist),1))
filelist = glob.glob(folder + '/' + cats_folder + '_test/*')
test_cats = np.array([np.array(imread(filename).flatten()) for filename in filelist])
test_cats_y = np.ones((len(filelist),1))

train_both = np.concatenate((train_dogs, train_cats), axis=0)

train_both_y = np.concatenate((train_dogs_y, train_cats_y), axis=0)
test_both = np.concatenate((test_dogs, test_cats), axis=0)

test_both_y = np.concatenate((test_dogs_y, test_cats_y), axis=0)

np.random.seed(1)
np.random.shuffle(train_both)
np.random.seed(1)
np.random.shuffle(train_both_y)
np.random.seed(2)
np.random.shuffle(test_both)
np.random.seed(2)
np.random.shuffle(test_both_y)

# Testdata in right format?
# imsave("out1.jpg", test_both[0].reshape(32,32,3))
# imsave("out2.jpg", test_both[1].reshape(32,32,3))
# imsave("out3.jpg", test_both[2].reshape(32,32,3))
# imsave("out4.jpg", test_both[3].reshape(32,32,3))
# 
# print(test_both_y[0])
# print(test_both_y[1])
# print(test_both_y[2])
# print(test_both_y[3])

# the data, shuffled and split between train and test sets
x_train = train_both.reshape(train_both.shape[0], img_rows,img_cols,img_channels)
y_train = train_both_y
x_test = test_both.reshape(test_both.shape[0], img_rows,img_cols,img_channels)
y_test = test_both_y
#mnist
#(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, img_channels)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, img_channels)
    input_shape = (img_rows, img_cols, img_channels)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices (-> one-hot-vectors)
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# revise [convnets](https://www.youtube.com/watch?v=GYGYnspV230)
# see <https://keras.io/layers/convolutional/#conv2d>

# inspiration for this net from [here](http://cs.stanford.edu/people/karpathy/convnetjs/demo/cifar10.html)
model = Sequential()
model.add(Conv2D(32, kernel_size=(7, 7),
                 activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(20, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
# 5x5 filter does not work here
model.add(Conv2D(20, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(20, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

# ///////// Added By @Mehdi
import json
file = open(file="result.json", mode="w")  
model_accuracy = np.float64(score[1])
res = {"accuracy" : model_accuracy}
json.dump(res, file)
file.close()
