from .model import *
from .loader import *
from .similarity import *
from .algorithms import *
from .wordcloud import *
import webbrowser
import json

def getAlgo(sim, algoVal):
	return (KMeans(sim) if algoVal == "1" 
						else DivisiveHC(sim))

def getParameter(paramVal):
	return (Following() if paramVal == "1" 
						else Hashtags() if paramVal == "2" 
						else Retweets())

def normalizedSimilarity(user1, user2, s):
	sim = s.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)

def lol(a, b):
	print("HI")

def start(paramVal, algoVal):
	loader = Loader("thesis/backend/Demo Tweet Data/", "user_dataset.json", "following.json", "tweets.json")
	sim = getParameter(paramVal)
	algo = getAlgo(sim, algoVal)
	clusterer = Clusterer(loader, algo)
	clusterer.run()
	communities = clusterer.communities
	userList = clusterer.users

	commNum = 1

	data = {}
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
	# print("FPUPC:", clusterer.fpupc())

	print("\nWriting json...")
	with open('vis.json', 'w') as outfile:
	    json.dump(data, outfile)

	print("Writing word cloud data...")
	with open('communitytweets.json', 'w') as outfile:
	    json.dump(communityTweets, outfile)

	countWords("communitytweets.json", "wordCounts.json")
	# url = "http://localhost:8000/Visualization/index.html?words=../wordCounts.json&graph=../vis.json&directed=" + ("true" if paramVal != "2" else "false")
	# webbrowser.open(url)	