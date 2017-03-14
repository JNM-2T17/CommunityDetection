from model import *
from loader import *
from similarity import *
from algorithms import *
import json

def normalizedSimilarity(user1, user2):
	f = Following()
	sim = f.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)

loader = Loader("Tweet Data/", "user_dataset.json", "following.json", "tweets.json")
following = Following()
algo = DivisiveHC(following)
clusterer = Clusterer(loader, algo)
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
		print("-", u.id, u.data["name"])
		node = {}
		node["name"] = u.data["name"]
		node["group"] = commNum
		data["nodes"].append(node)
		indices[u.id] = ctr
		ctr+=1

	commNum += 1


users = clusterer.users
for key in users:
	curUser = users[key]
	# if curUser.countNetworkSize()==0:
	# 	print(curUser.data["name"], "is irrelevant")
	for f in curUser.following:
		link = {}
		link["source"] = indices[curUser.id]
		link["target"] = indices[curUser.following[f].id]
		link["value"] = normalizedSimilarity(curUser, curUser.following[f])
		data["links"].append(link)

print("Finished! Generated", len(communities), "communities")
print("Modularity:", clusterer.modularity())
print("FPUPC:", clusterer.fpupc())

print("Writing json...")
with open('alron_vis.json', 'w') as outfile:
    json.dump(data, outfile)