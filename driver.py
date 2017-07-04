from model import *
from loader import *
from similarity import *
from algorithms import *
from wordcloud import *
import webbrowser
import json

def getAlgo(sim, algoVal):
	return (KMeans(sim) if algoVal == "1" 
						else DivisiveHC(sim))

def getParameter(paramVal):
	return (Following() if paramVal == "1" 
						else Hashtags() if paramVal == "2" 
						else Retweets() if paramVal == "3"
						else Mentions())

def normalizedSimilarity(user1, user2, s):
	sim = s.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)


print("Input algorithm:")
print("1- KMeans")
print("2- Divisive HC")
algoVal = input()

print("Input parameter:")
print("1- Following")
print("2- Hashtags")
print("3- Retweets")
print("4- Mentions")

paramVal = input()
print()
loader = Loader("Demo Tweet Data/", "user_dataset.json", "following.json", "tweets.json")
sim = getParameter(paramVal)
algo = getAlgo(sim, algoVal)
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

print()

for c in communities:
	print("Community #", commNum, "has", len(c.users), ("users" if len(c.users) > 1 else "user"))
	tweetString = []
	for u in c.users:
		# print("-", u.id)
		for t in u.tweets:
			tweetString.append(t.tweetdata["text"])
		node = {}
		node["name"] = u.data["id"]
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

print("\nFinished! Generated", len(communities), "communities")
print("Modularity:", clusterer.modularity())
print("DBI:", clusterer.dbi())
# print("FPUPC:", clusterer.fpupc())

print("\nWriting json...")
with open('vis.json', 'w') as outfile:
    json.dump(data, outfile)

print("Writing word cloud data...")
with open('communitytweets.json', 'w') as outfile:
    json.dump(communityTweets, outfile)

print("Opening visualization in web browser...")
countWords("communitytweets.json", "wordCounts.json")
url = "http://localhost:8000/Visualization/index.html?words=../wordCounts.json&graph=../vis.json&directed=" + ("true" if paramVal != "2" else "false")
webbrowser.open(url)