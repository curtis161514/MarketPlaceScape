from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd

def scrape():
	print('..*retrieving adds*...')
	browser = webdriver.Firefox(executable_path=r'/home/curtiswright/Documents/GulfAi/Marketplace/ATVs/geckodriver')
	browser.get('https://www.facebook.com/marketplace/category/powersports')
	
	sleep(45)

	# Get scroll height
	last_height = browser.execute_script("return document.body.scrollHeight")

	for s in range(9):
		# Scroll down to bottom
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		t = np.random.random()
		if t < 0.5:
			sleep(round(10 + np.random.random()*14,1))
		if t > 0.5:
			sleep(round(15 + np.random.random()*25,1))


		# Calculate new scroll height and compare with last scroll height
		new_height = browser.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


	#intiate empty lists for title and price
	titles = np.asarray([])
	prices = np.asarray([])

	#get titles
	title = browser.find_elements_by_xpath("//*[@class='idiwt2bm bixrwtb6 ni8dbmo4 stjgntxs k4urcfbm']")
	for k in title:
		titles = np.append(titles,k.get_attribute('alt'))

	#get prices
	price = browser.find_elements_by_xpath("//*[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 tia6h79c fe6kdd0r mau55g9w c8b282yb iv3no6db a5q79mjw g1cxx5fr lrazzd5p oo9gr5id']")
	for k in price:
		prices = np.append(prices,k.text)


	cost = pd.DataFrame(prices)
	add = pd.DataFrame(titles)
	data = pd.concat([add,cost],axis=1)
	data.to_csv('newdata',sep=',', header = ['List','Price'],index = False)
	print('found ',data.shape[0],' listings')
	sleep(5)
