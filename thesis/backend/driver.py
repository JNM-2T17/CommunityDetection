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
						else Retweets() if paramVal == "3"
 						else Mentions())

def normalizedSimilarity(user1, user2, s):
	sim = s.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)

def start(paramVal, algoVal):
	loader = Loader("thesis/backend/Demo Tweet Data/compressed.json")
	sim = getParameter(paramVal)
	algo = getAlgo(sim, algoVal)
	clusterer = Clusterer(loader, algo)
	clusterer.run()
	communities = clusterer.communities
	userList = clusterer.users

	commNum = 1

	data = {}
	data["directed"] = "false" if paramVal == "2" else "true"
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
	output = {}
	output['mod'] = math.ceil(clusterer.modularity()*1000)/1000
	output['algo'] = algoVal
	output['param'] = paramVal

	return output