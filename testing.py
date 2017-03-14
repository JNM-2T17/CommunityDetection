from model import *
from loader import *
from similarity import *
from algorithms import *
import json

loader = Loader("Tweet Data/", "user_dataset.json", "following.json", "tweets.json")
users = loader.load_user_friendships()
