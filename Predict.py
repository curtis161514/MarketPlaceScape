import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from PredictPreProcessor import predictpreprocess
from Scrape import scrape
from Train import train

#first number in the file path
modelnumber = str('50')

#run the scraper to get adds
scrape()

#process data and get predictions
boatmodel = load_model(modelnumber+'.0_ATVModel.h5')
datafile = 'newdata'
keyfile = modelnumber+'.0_keys.txt'
normfile = modelnumber+'.0_mean_std'
data,targets,titles = predictpreprocess(datafile,keyfile,normfile)
pred = boatmodel.predict(data)

#load unnormalization values
norm_val = pd.read_csv(normfile)
pred_price = pred*norm_val['stdev'][0]+norm_val['mean'][0]
actual_price = targets*norm_val['stdev'][0]+norm_val['mean'][0]
advantage = (pred_price.T/actual_price)[0]

#put the deals together and export to file
i = 0 
adds = np.asarray([])
pred_p = np.asarray([])
act_p = np.asarray([])

for adv in advantage:
	if adv > 2 and adv < 4:
		adds = np.append(adds,titles[i])
		pred_p = np.append(pred_p,pred_price[i])
		act_p = np.append(act_p,actual_price[i])
	i+=1


data = pd.DataFrame(adds)
data['Predicted'] = pd.DataFrame(pred_p)
data['Actual'] = pd.DataFrame(act_p)
data.to_csv('deals.csv',sep=',', header = ['Title','Predicted','Actual'], index = False)
print('found ',data.shape[0], ' deals.  look in deals.csv...')

#run the training model to update on new adds
train()
