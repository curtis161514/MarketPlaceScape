import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import Adam
from BoatPreProcessor import boatpreprocess,train_test_split

#####################################################
#-----------------------Preprocess data--------------
#####################################################

filename = 'data1'
trainsplit = .9
data,targets,mean_price,std_price = boatpreprocess(filename)
train_data,test_data,train_targets,test_targets = train_test_split(data,targets,trainsplit)

######################################################
#----------------build and fit NN---------------
########################################################

#clear previous model
tf.keras.backend.clear_session()

#Define model architecture
model = Sequential()

#design nn arcitecture
model.add(Dense(3, input_shape = (train_data.shape[1],), activation = 'tanh'))
#model.add(Dropout(0.5))
model.add(Dense(1, activation = 'tanh')) #, activation ='sigmoid'
 
# Compile model
model.compile(loss='mse', optimizer= 'Adam')
print(model.summary())

# Fit model on training data
model.fit(train_data, train_targets, 
          batch_size=100, epochs=50, verbose=1, validation_data = (test_data,test_targets))
 
# Evaluate model on test data
score = score = model.evaluate(test_data, test_targets, verbose=0)
score = round(score*100,0)
print(score)

#create unique string to save model to working directory
d = str(score) + '_BoatModel.h5'
model.save(d)

#create dataframe of max min mean and stdev values
max_min = {'mean':[mean_price],'stdev':[std_price]}
max_min = pd.DataFrame(max_min)
max_min.to_csv(str(score) + '_mean_std',sep=',', header = True)
