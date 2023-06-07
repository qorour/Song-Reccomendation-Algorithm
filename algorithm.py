import requests
import base64
import pandas as pd
from scipy.spatial.distance import euclidean

# Set the headers and data

data = {
} 

# TO DO: want to create a song reccomendation algorithm that goes off some interesting piece of data
# |-> thinking political quiz scores, easiest political compass: enter the values you got from the quiz then see what the algorithm would reccomend
# Getting some guidance from: https://towardsdatascience.com/a-simple-song-recommender-system-in-python-tutorial-3e4c111198d6

df = pd.read_csv('test-ratings-data.csv') 
#print(df)



def distance_form(person1,person2): # used to find person closest to song ratings to then help make predictions on new entry
  c = euclidean(person1,person2)
  return c

def closest_person(person):
  current = ratings.loc[person]
  print(current)
  closest_person=''
  closest_distance=float('inf')

  for p in ratings.itertuples():
    if p.Index==current:
      continue # if looking at current person, continue past them to find closest person that's not themself
    distance_to_other_person = distance_form(person,ratings.loc[p.Index])
    if distance_to_other_person < closest_distance:
      # new highest, so make it the new closest distnace
      closest_distance = distance_to_other_person
      closest_person = p.Index

  return closest_person

my_ratings = { 'Name':'Quinn',
               'Stronger Rating': 5,
               'CallMeMaybe Rating': 4,
               'RingOfFire Rating': 5,
               'StairwayToHeaven Rating': 2
}
df = df.append(my_ratings, ignore_index = True)
print(df)
ratings=df.fillna(3) # filling all nulls so doesn't ruin formula w/3 vals (neutral)

closest_distance=float('inf')
print("I'm most similar to:")
print(closest_person('Quinn'))
print(closest_distance)
