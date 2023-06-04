import requests
import base64
import pandas as pd

# Set the headers and data

data = {
} 

# TO DO: want to create a song reccomendation algorithm that goes off some interesting piece of data
# |-> thinking political quiz scores, easiest political compass: enter the values you got from the quiz then see what the algorithm would reccomend
# Getting some guidance from: https://towardsdatascience.com/a-simple-song-recommender-system-in-python-tutorial-3e4c111198d6

df = pd.read_csv('test-ratings-data.csv') 
print(df)