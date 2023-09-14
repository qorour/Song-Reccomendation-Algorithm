import requests
import base64
import pandas as pd
from scipy.spatial.distance import euclidean

# TO DO: want to create a song reccomendation algorithm that goes off some interesting piece of data
# |-> thinking political quiz scores, easiest political compass: enter the values you got from the quiz then see what the algorithm would reccomend
# Getting some guidance from: https://towardsdatascience.com/a-simple-song-recommender-system-in-python-tutorial-3e4c111198d6

def load_ratings(filename):
    try:
        return pd.read_csv(filename, index_col=0).fillna(3)  # Fill NaN values with neutral ratings (3)
    except FileNotFoundError: # should never encounter this but if change to a new file could be an issue
        print(f"File '{filename}' not found. Creating a new dataset.")
        return pd.DataFrame(columns=['Name', 'Stronger Rating', 'CallMeMaybe Rating', 'RingOfFire Rating', 'StairwayToHeaven Rating'])

def distance_form(person1,person2, ratings): # used to find person closest to song ratings to then help make predictions on new entry
  p1 = ratings.loc[person1]
  p2 = ratings.loc[person2]
  c = euclidean(p1,p2)
  return c

def closest_person(person,ratings):

  #current = ratings.loc[person]
  closest_person=''
  closest_distance=float('inf')

  for p in ratings.index:
    if p==person:
      continue # if looking at current person, continue past them to find closest person that's not themself
    distance_to_other_person = distance_form(person,p,ratings)
    if distance_to_other_person < closest_distance:
      # new highest, so make it the new closest distance
      closest_distance = distance_to_other_person
      closest_person = p

  return closest_person, closest_distance

def add_new_person(new_person, ratings):
  print(ratings)
  print("Welcome to the reccomender, new user ",new_person, "! Please rank the following songs on a scale from 1 to 5")
  # should be a for loop solution instead of having a new line of code for each column rating
  stronger_rating = input('Stronger by Kanye West (Hip Hop/Pop Rap)\n')
  callmemaybe_rating = input('Call Me Maybe by Carly Rae Jepsen (Pop)\n')
  ringoffire_rating = input('Ring of Fire by Johnny Cash (Country/Folk)\n')
  stairwaytoheaven_rating = input('Stairway to Heaven by Led Zeppelin (Rock)\n')
  new_row = {'Stronger Rating':stronger_rating, 'CallMeMaybe Rating':callmemaybe_rating, 'RingOfFire Rating':ringoffire_rating, 'StairwayToHeaven Rating':stairwaytoheaven_rating}
  ratings = ratings.append(pd.Series(new_row, name=new_person))
  print(ratings)
  closest_person(new_person,ratings)
  return "new person added"

def main():
  # made as its own function so can call back on it whenever we finish analyizing a name
  # TO DO: looks like appending new rating completely messes up index column. Find out how to add new entries easily.
  ratings = load_ratings('test-ratings-data.csv')

  my_ratings = { 'Name':'Quinn',
               'Stronger Rating': 5,
               'CallMeMaybe Rating': 4,
               'RingOfFire Rating': 5,
               'StairwayToHeaven Rating': 2
  }

  name = input('What is your name? You can also type "exit" to exit the program\n')
  # Check if person exists in dataset, run appropriate functions
  if name not in ratings.index:
    print("ERROR: user not registered")
    add_new_person(name, ratings)
    return
  elif name == "exit":
    print("GOODBYE!")
    return
  else:
    print("You are most similar to: ", closest_person(name,ratings)[0])
  print("with a similarity distance of: ", closest_person(name,ratings)[1])

if __name__ == "__main__":
    main()
