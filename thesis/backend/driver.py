from .model import *
from .loader import *
from .similarity import *
from .algorithms import *
from .wordcloud import *
import webbrowser
import json

def getAlgo(sim, algoVal, cosine, k):
	return (KMeans(sim,cosine, k) if algoVal == "1" 
						else DivisiveHC(sim, cosine) if algoVal == "2"
						else AgglomerativeHC(sim, cosine) if algoVal == "3"
						else AgglomerativeHCSA(sim, cosine) if algoVal == "4"
						else KMeansSA(sim, cosine) if algoVal == "5"
						else DivisiveHCSA(sim, cosine))

def getParameter(paramVal):
	return (Following() if paramVal == "1" 
						else Hashtags() if paramVal == "2" 
						else Retweets() if paramVal == "3"
 						else Mentions())

def getAlgoString(algoVal, kVal=0):
	if kVal==0:
		return ("K-Means" if algoVal == "1" 
						else "Divisive HC" if algoVal == "2"
						else "Agglomerative HC" if algoVal == "3"
						else "Agglomerative SA HC")
	else:
		return "K-Means (K="+kVal+")"

def getParamString(paramVal):
	return ("Following" if paramVal == "1" 
						else "Hashtags" if paramVal == "2" 
						else "Retweets" if paramVal == "3"
 						else "Mentions")

def normalizedSimilarity(user1, user2, s):
	sim = s.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)

def start(paramVal, algoVal, measureVal,k):
	# loader = Loader("thesis/backend/Actual Final Tweet Data/compressed.json")
	loader = Loader("thesis/backend/Demo Tweet Data/compressed.json")
	sim = getParameter(paramVal)
	algo = getAlgo(sim, algoVal,measureVal == "1",k if k is None else int(k))
	clusterer = Clusterer(loader, algo)
	clusterer.run()
	clusterer.cleanCommunities()
	communities = clusterer.communities
	userList = clusterer.users

	commNum = 1

	data = {}
	data["directed"] = "false" if paramVal == "2" else "true"
	data["nodes"] = []
	data["links"] = []
	data["communities"] = []
	data["communityLinks"] = []
	data["info"] = {"minSize" : float('Inf'), "maxSize" : 0}

	communityTweets = {}

	indices = {}
	commIndices = {}

	ctr = 0
	commCtr = 0

	print()

	for c in communities:
		print("Community #", commNum, "has", len(c.users), ("users" if len(c.users) > 1 else "user"))

		comm = {}
		comm["name"] = commNum
		comm["group"] = commNum
		comm["size"] = len(c.users)
		data["communities"].append(comm)

		if data["info"]["minSize"] > comm["size"]:
			data["info"]["minSize"] = comm["size"]

		if data["info"]["maxSize"] < comm["size"]:
			data["info"]["maxSize"] = comm["size"]

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
		communityTweets[commNum] = {"size" : len(c.users), "tweets" : tweetString}
		commNum += 1

	users = clusterer.users
	for key in users:
		curUser = users[key]
		for e in curUser.outgoingEdges:
			link = {}
			link["source"] = curUser.id
			link["target"] = e
			link["value"] = normalizedSimilarity(curUser, userList[e], sim)
			data["links"].append(link)
			# link["source"] = indices[curUser.id]
			# link["target"] = indices[e]
			# link["value"] = normalizedSimilarity(curUser, userList[e], sim)
			# data["links"].append(link)

	# TODO: Actually calculate distance between communities

	commCount = len(communities);

	for i in range(1, commCount + 1):
	 	for j in range(i+1, commCount + 1):
	 		link = {}
	 		link["source"] = i - 1
	 		link["target"] = j - 1
	 		linkVal = math.floor((clusterer.dbi2(i-1,j-1) - 1) / 2 * 100) + 2;
	 		if linkVal < 2:
	 			linkVal = 2
	 		link["value"] = linkVal
	 		data["communityLinks"].append(link)

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
	output['algo'] = getAlgoString(algoVal, k)
	output['param'] = getParamString(paramVal)
	output['dbi'] = math.ceil(clusterer.dbi() * 1000) / 1000
	if output['dbi'] == -1:
		output['dbi'] = 'N/A'

	return output