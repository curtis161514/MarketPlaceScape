import pandas as pd
import numpy as np 
import csv


def predictpreprocess(datafile,keyfile,normfile):

	#import data
	filename = datafile 
	data = pd.read_csv(filename).drop_duplicates()  

	#import norm values
	norm_val = pd.read_csv(normfile)

	#seperate out the city
	data['Title'], data['City'] = data['List'].str.split(' in ', 1).str

	#drop the list
	#data.drop(columns =["List"], inplace = True)

	#seperate year and name
	data['Year'], data['Name'] = data['Title'].str.split(' ', 1).str

	#drop title
	data.drop(columns =["Title","City"], inplace = True)

	#drop $ from price
	data['Price'] = data['Price'].map(lambda x: x.lstrip('$'))

	#drop , from price
	data['Price'] = data['Price'].str.replace(',', '', regex=True)

	#convert price and year to number
	data['Price'] =  pd.to_numeric(data['Price'], errors = 'coerce') 
	data['Year'] =  pd.to_numeric(data['Year'], errors = 'coerce') 

	#change name to all lowercase
	data['Name'] = data['Name'].str.lower()

	#make sure name is a string
	data['Name'] = data['Name'].astype(str)

	#drop bs price rows
	data.drop(data[data['Price'] < 300].index, inplace = True) 
	data.drop(data[data['Price'] == 123].index, inplace = True)
	data.drop(data[data['Price'] == 1234].index, inplace = True)
	data.drop(data[data['Price'] == 12345].index, inplace = True)
	data.drop(data[data['Price'] == 123456].index, inplace = True)
	data.drop(data[data['Price'] == 1234567].index, inplace = True)
	data.drop(data[data['Price'] == 11111].index, inplace = True)
	data.drop(data[data['Price'] == 1111].index, inplace = True)
	data.drop(data[data['Price'] == 99999].index, inplace = True)
	data.drop(data[data['Price'] > 20000].index, inplace = True)
	data.drop(data[data['Price'] =='FREE'].index, inplace = True)
	data.drop(data[data['Price'] =='Contact Seller'].index, inplace = True)

	#drop bs years
	data.drop(data[data['Year'] < 1970].index, inplace = True)

	#normalize year and price
	data['Year'] = (data['Year'] - 1960)/60
	data['Price'] = (data['Price'] - norm_val['mean'][0])/ norm_val['stdev'][0]

	#drop any nan values
	data = data.dropna()

	#reset index
	data.reset_index(drop = True,inplace=True)
	
	#convert names to an array so they can be further processed below
	titles = np.asarray(data['List'],dtype = str)

	########################################################
	#bring in keys and create sparce matrix
	############################################################

	#load keys into a list
	key_list = []
	with open(keyfile, newline='') as csvfile:
		keys = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in keys:
			key_list.append(row)

	#initalize numpy arrays
	num_adds = data.shape[0]
	num_keys = len(key_list)
	sparce_data = np.zeros((num_adds,num_keys+1), dtype = 'float32')

	#populate sparce matrix - takes some time...
	for add in range(num_adds):
		key_index_count = 0
		for key_index in key_list:
			key_index_count+=1
			for key in key_index:
				if key in data['Name'][add]:
					sparce_data[add,key_index_count] = 1
		print('pre-processing ',add+1,' of ',num_adds,' valid listings')

	#bring year into the sparce matrix
	for add in range(num_adds):
		sparce_data[add,0] = data['Year'][add]

	#create a targets column
	targets = np.asarray(data['Price'], dtype = 'float32')

	#make sure sparce data is a float32 np array
	sparce_data = np.asarray(sparce_data,dtype = 'float32')

	#delete any adds with no keyword matches
	index = 0
	no_hits = np.asarray([])
	for row in sparce_data:
		if sum(row)<2:
			no_hits = np.append(no_hits,index)
		index+=1
	
	sparce_data = np.delete(sparce_data,no_hits,0)
	targets = np.delete(targets,no_hits,0)
	titles = np.delete(titles,no_hits,0)		
	
	return sparce_data,targets,titles