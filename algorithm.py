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

df = pd.read_csv('test-ratings-data.csv', index_col=0) 
#print(df)

my_ratings = { 'Name':'Quinn',
               'Stronger Rating': 5,
               'CallMeMaybe Rating': 4,
               'RingOfFire Rating': 5,
               'StairwayToHeaven Rating': 2
}

# TO DO: looks like appending new rating completely messes up index column. Find out how to add new entries easily.
print(my_ratings)
#df = df.append(my_ratings, ignore_index = True)
print(df)
ratings=df.fillna(3) # filling all nulls w/3 vals (neutral) so doesn't ruin formula


def distance_form(person1,person2): # used to find person closest to song ratings to then help make predictions on new entry
  print("distance form time")
  print(person2)
  print(ratings.loc[person2])
  p1 = ratings.loc[person1]
  p2 = ratings.loc[person2]
  c = euclidean(p1,p2)
  return c

def closest_person(person):
  current = ratings.loc[person]
  closest_person=''
  closest_distance=float('inf')

  for p in ratings.index:
    print("curr p1:")
    print(p)
    print("curr p2:")
    print(current)
    print("curr p3:")
    print(person)
    if p==person:
      print("curr p continue found")
      continue # if looking at current person, continue past them to find closest person that's not themself
    print("curr not the same one/is different")
    distance_to_other_person = distance_form(person,p)
    if distance_to_other_person < closest_distance:
      print("curr p lower found")
      # new highest, so make it the new closest distance
      closest_distance = distance_to_other_person
      closest_person = p

  return closest_person

closest_distance=float('inf')
print("I'm most similar to:")
print(closest_person('Farmer Pete'))
print(closest_distance)
