import pandas as pd
from tensorflow.keras.models import load_model
from BoatPreProcessor import boatpreprocess


#load data and get predictions
boatmodel = load_model('50.0_BoatModel.h5')
filename = 'testdata'
data,targets,mean_price,std_price = boatpreprocess(filename)
pred = boatmodel.predict(data)

#load unnormalization values
norm_val = pd.read_csv('50.0_mean_std')
dollars = pred*norm_val['stdev'][0]+norm_val['mean'][0]
print(dollars)