from model import *
from Loader import *
from Similarity import *
from KMeans import *
from dhc import *
import json

def normalizedSimilarity(user1, user2):
	f = Following()
	sim = f.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10)

loader = Loader("MongoDB Tweet Data/", "user.json", "following.json")
following = Following()
kmeans = divisive_hc(following)
clusterer = Clusterer(loader, kmeans)
clusterer.run()
communities = clusterer.communities

commNum = 1

data = {}
data["directed"] = False
data["nodes"] = []
data["links"] = []

indices = {}

ctr = 0
for c in communities:
	print("\nCommunity #", commNum)

	for u in c.users:
		print("-", u.id)
		node = {}
		node["name"] = u.id
		node["group"] = commNum
		data["nodes"].append(node)
		indices[u.id] = ctr
		ctr+=1

	commNum += 1


users = clusterer.users
for key in users:
	curUser = users[key]
	for f in curUser.following:
		link = {}
		link["source"] = indices[curUser.id]
		link["target"] = indices[curUser.following[f].id]
		link["value"] = normalizedSimilarity(curUser, curUser.following[f])
		data["links"].append(link)

print("Finished!")
print("Modularity:", clusterer.modularity())
print("FPUPC:", clusterer.fpupc())

print("Writing json...")
with open('vis.json', 'w') as outfile:
    json.dump(data, outfile)