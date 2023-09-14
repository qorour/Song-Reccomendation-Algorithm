import requests
import base64
import pandas as pd
from scipy.spatial.distance import euclidean

# Project idea/basic guidance from: https://towardsdatascience.com/a-simple-song-recommender-system-in-python-tutorial-3e4c111198d6

class SongRecommender:
  def __init__(self, filename):
        # begins instance with new filename and immediately loads it, only then do we run main
        self.filename = filename
        self.ratings = self.load_ratings()

  def load_ratings(self):
    try:
        return pd.read_csv(self.filename, index_col=0).fillna(3)  # Fill NaN values with neutral ratings (3)
    except FileNotFoundError: # should never encounter this but if change to a new file could be an issue
        print(f"ERROR: file not found. Creating a new empty dataset...")
        return pd.DataFrame(columns=['Name', 'Stronger Rating', 'CallMeMaybe Rating', 'RingOfFire Rating', 'StairwayToHeaven Rating'])

  def distance_form(self,person1,person2): # used to find person closest to song ratings to then help make predictions on new entry
    p1 = self.ratings.loc[person1]
    p2 = self.ratings.loc[person2]
    c = euclidean(p1,p2)
    return c

  def closest_person(self,person):
    closest_person=''
    closest_distance=float('inf')

    for p in self.ratings.index:
      if p==person:
        continue # if looking at current person, continue past them to find closest person that's not themself
      distance_to_other_person = self.distance_form(person,p)
      if distance_to_other_person < closest_distance:
        # new highest, so make it the new closest distance
        closest_distance = distance_to_other_person
        closest_person = p

    return closest_person, closest_distance

  def add_new_person(self,new_person):
    print(self.ratings)
    print("Welcome to the reccomender, new user",new_person,"! Please rank the following songs on a scale from 1 to 5")
    # should be a for loop solution? instead of having a new line of code for each column rating, try to implement later
    while True:
      try:
        stronger_rating = int(input('Stronger by Kanye West (Hip Hop/Pop Rap)\n')) 
        callmemaybe_rating = int(input('Call Me Maybe by Carly Rae Jepsen (Pop)\n'))
        ringoffire_rating = int(input('Ring of Fire by Johnny Cash (Country/Folk)\n'))
        stairwaytoheaven_rating = int(input('Stairway to Heaven by Led Zeppelin (Rock)\n'))
        break
      except ValueError:
        print("ERROR: please only integers! restarting rating collection...")  
    new_row = {'Stronger Rating':stronger_rating, 'CallMeMaybe Rating':callmemaybe_rating, 'RingOfFire Rating':ringoffire_rating, 'StairwayToHeaven Rating':stairwaytoheaven_rating}
    self.ratings = self.ratings.append(pd.Series(new_row, name=new_person))
    print(self.ratings)
    close_person,close_distance = self.closest_person(new_person)
    print("You are closest to: ",close_person," and have a distance of",close_distance)
    return self.ratings

  def main(self):
    # made as its own function so can call back on it whenever we finish analyizing a name
    # TO DO: looks like appending new rating completely messes up index column. Find out how to add new entries easily.
    #ratings = self.load_ratings('test-ratings-data.csv')

    flag = 0 #keeping flag in case want to add more ends to the program vs just the exit command
    while (flag == 0):
      name = input('What name would you like to lookup? You can also type "exit" to exit the program\n')
      # Check if person exists in dataset, run appropriate functions
      if name == "exit":
        print("GOODBYE!")
        flag = 1
        #return
      elif name not in self.ratings.index:
        print("ERROR: user not registered")
        self.add_new_person(name)
      else:
        print("You are most similar to: ", self.closest_person(name)[0])
        print("with a similarity distance of: ", self.closest_person(name)[1])

if __name__ == "__main__":
    recommender = SongRecommender('test-ratings-data.csv')
    recommender.main()
    #main()
