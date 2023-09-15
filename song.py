import requests
import base64
import pandas as pd
from scipy.spatial.distance import euclidean

class Song:
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre