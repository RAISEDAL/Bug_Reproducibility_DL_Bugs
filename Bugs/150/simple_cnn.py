import time

import numpy as np

from keras.datasets import cifar10
from keras.models import Model
from keras.layers import Dense, Dropout, Flatten, Convolution2D, MaxPooling2D, Input
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, EarlyStopping

batch_size = 32
num_classes = 10
epochs = 2
STAMP = 'simple_cnn'

(x_train, y_train), (x_val, y_val) = cifar10.load_data()
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_val.shape[0], 'test samples')

y_train = np_utils.to_categorical(y_train, num_classes)
y_val = np_utils.to_categorical(y_val, num_classes)

x_train = x_train.astype('float32')
x_val = x_val.astype('float32')
x_train /= 255
x_val /= 255

input_layer = Input(shape=(x_train.shape[1:]))

#Block 1
conv1 = Convolution2D(32,(7,7),
	padding='same',
	activation='relu')(input_layer)
conv2 = Convolution2D(32,(7,7),
	padding='same',
	activation='relu')(conv1)
pool1 = MaxPooling2D(pool_size=(2,2))(conv2)
drop1 = Dropout(0.25)(pool1)

#Block 2
conv3 = Convolution2D(64,(3,3),
	padding='same',
	activation='relu')(drop1)
conv4 = Convolution2D(64,(3,3),
	padding='same',
	activation='relu')(conv3)
pool2 = MaxPooling2D(pool_size=(2,2))(conv4)
drop2 = Dropout(0.25)(pool2)

#Block 3
conv5 = Convolution2D(128,(1,1),
	padding='same',
	activation='relu')(drop2)
conv6 = Convolution2D(128,(1,1),
	padding='same',
	activation='relu')(conv5)
pool3 = MaxPooling2D(pool_size=(2,2))(conv6)
drop3 = Dropout(0.25)(pool3)

#Dense
flat = Flatten()(drop3)
dense1 = Dense(512,
	activation='relu')(flat)
drop4 = Dropout(0.5)(dense1)
output = Dense(num_classes,
	activation='softmax')(drop4)

model = Model(inputs=input_layer, outputs=output)


model.summary()
model.compile(loss='categorical_crossentropy',
	optimizer='adam',
	metrics=['accuracy'])

model_json = model.to_json()
with open('model/' + STAMP + ".json", "w") as json_file:
    json_file.write(model_json)
    
early_stopping = EarlyStopping(monitor='val_loss',
	patience=10,
	verbose=1)

bst_model_path = 'model/' + STAMP + '.h5'
model_checkpoint = ModelCheckpoint(bst_model_path,
    monitor='val_acc',
    verbose=1,
    save_best_only=True,
    save_weights_only=True)

#================================================== Train the Model =============================================================
print('Start training.')
start_time = time.time()

model.fit(x_train, y_train,
	batch_size=batch_size,
	epochs=epochs,
	validation_data=(x_val, y_val),
	shuffle=True,
	callbacks=[early_stopping, model_checkpoint])

score = model.evaluate(x_val,y_val,verbose=0)
end_time = time.time()
print("--- Training time: %s seconds ---" % (end_time - start_time))
print('Test score:', score[0])
print('Test accuracy:', score[1])
