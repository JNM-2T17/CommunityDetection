from model import *
from loader import *
from similarity import *
from algorithms import *
import json

def avgMod(modularity):
	total = 0.0
	for m in modularity:
		total+=m
	total/=len(modularity)
	return total

loader = Loader("Demo Tweet Data/", "user_dataset.json", "following.json", "tweets.json")

followingMod = []
followingCommCount = []
for i in range(0, 5):
	sim = Following()
	algo = KMeans(sim)
	clusterer = Clusterer(loader, algo)
	clusterer.run()
	followingMod.append(clusterer.modularity())
	followingCommCount.append(len(clusterer.communities))

hashMod = []
hashCommCount = []
for i in range(0, 5):
	sim = Hashtags()
	algo = KMeans(sim)
	clusterer = Clusterer(loader, algo)
	clusterer.run()
	hashMod.append(clusterer.modularity())
	hashCommCount.append(len(clusterer.communities))

retweetMod = []
retweetCommCount = []
for i in range(0, 5):
	sim = Retweets()
	algo = KMeans(sim)
	clusterer = Clusterer(loader, algo)
	clusterer.run()
	retweetMod.append(clusterer.modularity())
	retweetCommCount.append(len(clusterer.communities))

print("Experiment #A1: KMeans/Following Similarity")
for i in range(0, 5):
	print("Run", i, ": Modularity =", followingMod[i])
print("Average modularity:", avgMod(followingMod))
print("Average community count:", avgMod(followingCommCount))

print("Experiment #A2: KMeans/Hashtag Similarity")
for i in range(0, 5):
	print("Run", i, ": Modularity =", hashMod[i])
print("Average modularity:", avgMod(hashMod))
print("Average community count:", avgMod(hashCommCount))

print("Experiment #A3: KMeans/Retweeting Similarity")
for i in range(0, 5):
	print("Run", i, ": Modularity =", retweetMod[i])
print("Average modularity:", avgMod(retweetMod))
print("Average community count:", avgMod(retweetCommCount))