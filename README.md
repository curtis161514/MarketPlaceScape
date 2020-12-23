# MarketPlaceScape
Running Predict.py open market place and scrapes the ATV section for titles and prices.  It compares them to what an AI predicts the price should be and then saves all the good deals into a deals.csv file for further inspection.  Then it takes any new data and adds it to the data1 bank to re-train the model on all the new data that was scraped.  The whole code takes 1hr+ to run, mainly because of the random timers built into the scraper to avoid detection by fb.  As you see errors in the predictions, you can add or subtract words to the keys.txt file to help account for the errors.  The keys.txt is a list of key words to search for.  It serves as the pattern for 1-hot encoding the keywords into the arrays fed to the nueral net.  The neural net arcitecture is automatically updated when a keyword is changed, added, or deleted.   To use a newly trained model,  you need to update the number of the model,and key file.  The first line in predict.py (ex '50')  The '50' corresponds to the mean squared error of the model * 100.   49.0_model.h5 would means with mean squared error of 0.49 standard deviations.  you can open the mean_std file to see what the mean and standard deviation of prices are.
