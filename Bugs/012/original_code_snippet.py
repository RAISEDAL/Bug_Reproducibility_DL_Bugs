model = Sequential()
model.add( LSTM( 512, input_shape=(45, 2), return_sequences=True))
model.add( LSTM( 512, return_sequences=True))
model.add( (Dense(1)))
model.compile(loss='mse', optimizer='adam')
history = model.fit( X_train, y_train, batch_size = batchSize, epochs=epochs, shuffle = False)