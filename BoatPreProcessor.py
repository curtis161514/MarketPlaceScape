
import pandas as pd
import numpy as np 
import csv


def boatpreprocess(filename):

	#import data
	filename = filename 
	data = pd.read_csv(filename).drop_duplicates()  
	#data.to_csv('data2', header = True, index = False)

	#seperate out the city
	data['Title'], data['City'] = data['List'].str.split(' in ', 1).str

	#drop the list
	data.drop(columns =["List"], inplace = True)

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
	data['Year'] =  pd.to_numeric(data['Year']) 

	#change name to all lowercase
	data['Name'] = data['Name'].str.lower()

	#make sure name is a string
	data['Name'] = data['Name'].astype(str)

	#drop bs price rows
	data.drop(data[data['Price'] < 50].index, inplace = True) 
	data.drop(data[data['Price'] == 123].index, inplace = True)
	data.drop(data[data['Price'] == 1234].index, inplace = True)
	data.drop(data[data['Price'] == 12345].index, inplace = True)
	data.drop(data[data['Price'] == 123456].index, inplace = True)
	data.drop(data[data['Price'] == 1234567].index, inplace = True)
	data.drop(data[data['Price'] == 11111].index, inplace = True)
	data.drop(data[data['Price'] == 1111].index, inplace = True)
	data.drop(data[data['Price'] == 99999].index, inplace = True)
	data.drop(data[data['Price'] > 100000].index, inplace = True)
	data.drop(data[data['Price'] =='FREE'].index, inplace = True)
	data.drop(data[data['Price'] =='Contact Seller'].index, inplace = True)

	#drop bs years
	data.drop(data[data['Year'] < 1970].index, inplace = True)

	#normalize year and price
	mean_price = data['Price'].mean()
	std_price = data['Price'].std()
	data['Year'] = (data['Year'] - 1960)/60
	data['Price'] = (data['Price'] - data['Price'].mean()) / data['Price'].std()

	#drop any nan values
	data = data.dropna()

	#reset index
	data.reset_index(drop = True,inplace=True)

	########################################################
	#bring in keys and create sparce matrix
	############################################################

	#load keys into a list
	key_list = []
	with open('keys.txt', newline='') as csvfile:
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
		if sum(row)<1:
			no_hits = np.append(no_hits,index)
		index+=1
	
	sparce_data = np.delete(sparce_data,no_hits,0)
	targets = np.delete(targets,no_hits,0)
			
	return sparce_data,targets,mean_price,std_price

def train_test_split(sparce_data,targets,trainsplit):
	spl = 1/trainsplit	
	split = int(sparce_data.shape[0]//spl)
	permutation = np.random.permutation(sparce_data.shape[0])
	train_data = sparce_data[permutation][0:split]
	test_data = sparce_data[permutation][split:sparce_data.shape[0]]
	train_targets = targets[permutation][0:split]
	test_targets = targets[permutation][split:sparce_data.shape[0]]		

	return train_data,test_data,train_targets,test_targets