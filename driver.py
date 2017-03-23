from model import *
from loader import *
from similarity import *
from algorithms import *
import json

def normalizedSimilarity(user1, user2, s):
	sim = s.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)

loader = Loader("Tweet Data/", "user_dataset.json", "following.json", "tweets.json")
sim = Retweets()
algo = DivisiveHC(sim)
clusterer = Clusterer(loader, algo)
clusterer.run()
communities = clusterer.communities
userList = clusterer.users

commNum = 1

data = {}
data["directed"] = False
data["nodes"] = []
data["links"] = []

communityTweets = {}

indices = {}

ctr = 0
for c in communities:
	print("\nCommunity #", commNum)
	tweetString = []
	for u in c.users:
		try:
			print("-", u.id, u.data["name"])
		except UnicodeEncodeError:
			print("-", u.id)
		for t in u.tweets:
			tweetString.append(t.tweetdata["text"])
		node = {}
		node["name"] = u.data["name"]
		node["group"] = commNum
		data["nodes"].append(node)
		indices[u.id] = ctr
		ctr+=1
	communityTweets[commNum] = tweetString
	commNum += 1


users = clusterer.users
for key in users:
	curUser = users[key]
	for e in curUser.outgoingEdges:
		link = {}
		link["source"] = indices[curUser.id]
		link["target"] = indices[e]
		link["value"] = normalizedSimilarity(curUser, userList[e], sim)
		data["links"].append(link)

print("Finished! Generated", len(communities), "communities")
print("Modularity:", clusterer.modularity())
print("FPUPC:", clusterer.fpupc())

print("Writing json...")
with open('vis.json', 'w') as outfile:
    json.dump(data, outfile)

print("Writing word cloud data...")
# for x in communityTweets:
# 	communityTweets[x] = communityTweets[x][:5]
with open('communitytweets.json', 'w') as outfile:
    json.dump(communityTweets, outfile)