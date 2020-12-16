from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd



browser = webdriver.Firefox(executable_path=r'/home/curtiswright/Documents/GulfAi/Marketplace/geckodriver')
browser.get('https://www.facebook.com/marketplace/category/boats')

sleep(60)


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


data = pd.DataFrame(prices,titles)
data.to_csv('new',sep=',', header = True)
data.shape
