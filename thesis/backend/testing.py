from model import *
from loader import *
from similarity import *
from algorithms import *
import json

loader = Loader("Tweet Data/", "user_dataset.json", "following.json", "tweets.json")
sim = Hashtags()
algo = DivisiveHC(sim)
clusterer = Clusterer(loader, algo)

users = clusterer.users
for i in users:
	u = users[i]
	print(u.data["name"])
	for j in users:
		u2 = users[j]
		if len(sim.commonHashtags(u, u2))>0:
			print(u.data["name"], "has edge with", u2.data["name"], "sim =", sim.similarity(u, u2))
	print()