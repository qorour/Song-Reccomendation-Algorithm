import requests
import base64
import pandas as pd
from scipy.spatial.distance import euclidean

class User:
    def __init__(self, name):
        self.name = name
        self.ratings = {}