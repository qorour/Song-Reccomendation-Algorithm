import requests
import base64
import pandas as pd
from scipy.spatial.distance import euclidean

from song import Song
from user import User

# Project idea/basic guidance from: https://towardsdatascience.com/a-simple-song-recommender-system-in-python-tutorial-3e4c111198d6

class SongRecommender:
  def __init__(self, filename):
        # begins instance with new filename and immediately loads it, only then do we run main
        self.filename = filename
        # and store instances of songs/users in dictonaries for in depth info collection/future expansion
        self.songs = {}
        self.users = {}
        # finally, let's load all this data up!
        self.load_ratings()

  def load_ratings(self):
    try:
        self.ratings = pd.read_csv(self.filename, index_col=0).fillna(3)  # Fill NaN values with neutral ratings (3)
    except FileNotFoundError: # should never encounter this but if change to a new file could be an issue
        print(f"ERROR: file not found. Creating a new empty dataset...")
        self.ratings =  pd.DataFrame(columns=['Name'])

    # now load the existing users/songs into User and Song objects
    for user_name in self.ratings.index:
      if user_name not in self.users:
        self.users[user_name] = User(user_name)
      # make sure to keep track of ratings for each individual user
      user_obj = self.users[user_name]
      for song_name in self.ratings.columns:
        rating = self.ratings.at[user_name, song_name]
        user_obj.ratings[song_name] = rating
        if song_name not in self.songs and song_name != 'Name': # check the 'Name' just in case it accidently will overwrite all names later in program
          self.songs[song_name] = Song(song_name, "NA") # don't know genre info, could update functionality in future to get info on genre

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
        neighbor_highest_rated_song = max(self.users[p].ratings, key=self.users[p].ratings.get)

    return closest_person, closest_distance, neighbor_highest_rated_song

  def add_new_person(self,new_person):
    user_instance = User(new_person)
    self.users[new_person] = user_instance

    print("Welcome to the reccomender, new user",new_person,"! On a scale of 1 to 5, please rate...")
    for song_name in self.songs:
      while True:
        try:
          rating = int(input(f"Please Rate:'{song_name}' ({self.songs[song_name].genre})"))
          if (rating >= 1 or rating <= 5):
            break
          else:
            print("ERROR: please rate from 1 to 5")
        except ValueError:
          print("ERROR: please enter an integer rating.")
      user_instance.ratings[song_name] = rating 
    
    self.update_ratings()
    close_person,close_distance,highest_rate = self.closest_person(new_person)
    print("You are closest to: ",close_person," and have a distance of",str(round(close_distance, 2)),". Their favorite song was",highest_rate,". Give it a chance!")
    return self.ratings

  def add_new_song(self, song_name, genre):
    if song_name not in self.songs:
        song_obj = Song(song_name, genre)
        self.songs[song_name] = song_obj

        # now adds this song to all user's ratings (will default to 3 (neutral) for users who haven't rated it)
        for user_name in self.users:
            if song_name not in self.users[user_name].ratings:
                self.users[user_name].ratings[song_name] = 3

        self.update_ratings()
        print(f"Song '{song_name}' ({genre}) has been added.")
    else:
        print("ERROR: this song already exists!")

  def update_ratings(self):
    # this function will update new ratings/new songs of a new user into a new user object
    data = []
    for user_name in self.users:
        user_instance = self.users[user_name]
        row = {'Name': user_name}
        for song_name in self.songs:
          row[song_name] = user_instance.ratings.get(song_name, 3)  # defaults to 3 if not rated
        data.append(row)
    # now add our newly updated data to the ratings dataframe
    self.ratings = pd.DataFrame(data).set_index('Name')

  def main(self):
    flag = 0 #keeping flag in case want to add more ends to the program vs just the exit command
    while (flag == 0):
      name = input('What name would you like to lookup? You can also type "exit" to exit the program or "print" to see the ratings dataframe\n')
      # Check if person exists in dataset, run appropriate functions
      if name == "exit":
        print("GOODBYE!")
        flag = 1
        return
      elif name == "print":
        print(self.ratings)
      elif name not in self.ratings.index:
        print("ERROR: user not registered")
        self.add_new_person(name)
      else:
        close_person,close_distance,highest_rate = self.closest_person(name)
        print("You are most similar to: ", close_person)
        print("with a similarity distance of: ", str(round(close_distance, 2)))
        print("Their favorie song was",highest_rate,". You should give it a try!")

      # Now ask if we want to add any new songs. 
      new_song_q = input("Would you like to add a new song? Type 'Y' if yes\n")
      if new_song_q.upper() == "Y":
                song_name = input("What's the name of the song?: ")
                genre = input("What's the genre of the song?: ")
                self.add_new_song(song_name, genre)
                print("Your song has been added to the data! Let's get to rating...\n")

if __name__ == "__main__":
    recommender = SongRecommender('test-ratings-data.csv') #can have a file with user lists on it or just empty
    recommender.main()
