import shutil
from time import sleep
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam,RMSprop
from TrainPreProcessor import trainpreprocess,train_test_split

def train():
	print('Updating model with new data from the scrape')
	sleep(5)
	#####################################################
	#-----------------------Preprocess data--------------
	#####################################################

	datafile = 'data1'
	keyfile = 'keys.txt'
	trainsplit = .8
	data,targets,mean_price,std_price = trainpreprocess(datafile,keyfile)
	train_data,test_data,train_targets,test_targets = train_test_split(data,targets,trainsplit)

	######################################################
	#----------------build and fit NN---------------
	########################################################

	#clear previous model
	tf.keras.backend.clear_session()

	#Define model architecture
	model = Sequential()

	#design nn arcitecture
	model.add(Dense(7, input_shape = (train_data.shape[1],), activation = 'tanh'))
	model.add(Dropout(0.3))
	model.add(Dense(7, input_shape = (train_data.shape[1],), activation = 'tanh'))
	model.add(Dropout(0.3))
	model.add(Dense(1, activation = 'linear')) #, activation ='sigmoid'
	
	# Compile model
	model.compile(loss='mse', optimizer= 'Adam')
	print(model.summary())

	# Fit model on training data
	model.fit(train_data, train_targets, 
			batch_size=100, epochs=100, verbose=1, validation_data = (test_data,test_targets))
	
	# Evaluate model on test data
	score = score = model.evaluate(test_data, test_targets, verbose=0)
	score = round(score*100,0)

	#create unique string to save model to working directory
	d = str(score) + '_ATVModel.h5'
	model.save(d)

	#create dataframe of max min mean and stdev values
	max_min = {'mean':[mean_price],'stdev':[std_price]}
	max_min = pd.DataFrame(max_min)
	max_min.to_csv(str(score) + '_mean_std',sep=',', header = True)

	#save key file
	shutil.copy('keys.txt', str(score)+'_keys.txt')

