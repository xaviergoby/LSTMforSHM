from random import random
from random import randint
from numpy import array
from numpy import zeros
# from keras.models import Sequential
# from keras.layers import Conv2D
# from keras.layers import MaxPooling2D
# from keras.layers import LSTM
# from keras.layers import Dense
# from keras.layers import Flatten
# from keras.layers import TimeDistributed

# generate the next frame in the sequence
def next_frame(last_step, last_frame, column):
	# define the scope of the next step
	lower = max(0, last_step-1)
	upper = min(last_frame.shape[0]-1, last_step+1)
	# choose the row index for the next step
	step = randint(lower, upper)
	# copy the prior frame
	frame = last_frame.copy()
	# add the new step
	frame[step, column] = 1
	return frame, step

# generate a sequence of frames of a dot moving across an image
def build_frames(size):
	frames = list()
	# create the first frame
	frame = zeros((size,size))
	step = randint(0, size-1)
	# decide if we are heading left or right
	right = 1 if random() < 0.5 else 0
	col = 0 if right else size-1
	frame[step, col] = 1
	frames.append(frame)
	# create all remaining frames
	for i in range(1, size):
		col = i if right else size-1-i
		frame, step = next_frame(step, frame, col)
		frames.append(frame)
	return frames, right

# generate multiple sequences of frames and reshape for network input
cnt = 0
def generate_examples(size, n_patterns):
	cnt = 0
	X, y = list(), list()
	for _ in range(n_patterns):
		cnt = cnt + 1
		print(cnt)
		frames, right = build_frames(size)
		X.append(frames)
		y.append(right)
	# resize as [samples, timesteps, frame_width, frame_height, frame_channels]
	X = array(X).reshape(n_patterns, size, size, size, 1)
	y = array(y).reshape(n_patterns, 1)
	return X, y

# configure problem
size = 50

# define the conv_lstm_model
# conv_lstm_model = Sequential()
# conv_lstm_model.add(TimeDistributed(Conv2D(2, (2,2), activation='relu'), cnn_model_input_tensor_shape=(None,size,size,1)))
# conv_lstm_model.add(TimeDistributed(MaxPooling2D(pool_size=(2, 2))))
# conv_lstm_model.add(TimeDistributed(Flatten()))
# conv_lstm_model.add(LSTM(50))
# conv_lstm_model.add(Dense(1, activation='sigmoid'))
# conv_lstm_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
# print(conv_lstm_model.summary())

# fit conv_lstm_model
res = generate_examples(50, 5000)
X = res[0]
y = res[1]
# X_train, y_train = generate_examples(size, 5000)
print(X.shape)
print(y.shape)
# conv_lstm_model.fit(X_train, y_train, batch_size=32, epochs=1)

# evaluate conv_lstm_model
# X_train, y_train = generate_examples(size, 100)
# loss, acc = conv_lstm_model.evaluate(X_train, y_train, verbose=0)
# print('loss: %f, acc: %f' % (loss, acc*100))

# prediction on new data
# X_train, y_train = generate_examples(size, 1)
# yhat = conv_lstm_model.predict_classes(X_train, verbose=0)
# expected = "Right" if y_train[0]==1 else "Left"
# predicted = "Right" if yhat[0]==1 else "Left"
# print('Expected: %s, Predicted: %s' % (expected, predicted))