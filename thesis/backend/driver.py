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
	if kVal is None or kVal==0:
		return ("K-Means" if algoVal == "1" 
						else "Divisive HC" if algoVal == "2"
						else "Agglomerative HC" if algoVal == "3"
						else "Agglomerative SA HC" if algoVal == "4"
						else "K-Means SA" if algoVal == "5"
						else "Divisive SA HC")
	else:
		return "K-Means (K=%d)" % kVal

def getParamString(paramVal):
	return ("Following" if paramVal == "1" 
						else "Hashtags" if paramVal == "2" 
						else "Retweets" if paramVal == "3"
 						else "Mentions")

def getMeasureString(measureVal):
	return ("Cosine Similarity" if measureVal == "1" 
						else "Standard Similarity")

def normalizedSimilarity(user1, user2, s):
	sim = s.similarity(user1, user2)
	sim *= 100
	sim = int(sim)
	return int(sim/10 + 1)

def start(paramVal, algoVal, measureVal,k):
	loader = Loader("thesis/backend/Actual Final Tweet Data/compressed.json")
	# loader = Loader("thesis/backend/Demo Tweet Data/compressed.json")
	sim = getParameter(paramVal)
	k = k if k is None else int(k)
	algo = getAlgo(sim, algoVal,measureVal == "1",k)
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

	stats = {} # Statistics for each community e.g. number of users per location
	stats["location"] = {}

	communityTweets = {}
	communityProfile = {}

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

		stats["location"][commNum] = {}

		if data["info"]["minSize"] > comm["size"]:
			data["info"]["minSize"] = comm["size"]

		if data["info"]["maxSize"] < comm["size"]:
			data["info"]["maxSize"] = comm["size"]

		tweetString = []
		profileString = []
		for u in c.users:
			for t in u.tweets:
				tweetString.append(t.tweetdata["text"])

			profileString.append(u.data["description"])

			node = {}
			node["name"] = u.data["id"]
			node["group"] = commNum
			data["nodes"].append(node)
			indices[u.id] = ctr
			ctr+=1

			# Record number of users per location
			userLoc = u.data["location"].strip()
			if len(userLoc) == 0:
				userLoc = "N/A"
			if userLoc in stats["location"][commNum]:
				stats["location"][commNum][userLoc] = stats["location"][commNum][userLoc] + 1
			else:
				stats["location"][commNum][userLoc] = 1

		communityTweets[commNum] = {"size" : len(c.users), "string" : tweetString}
		communityProfile[commNum] = {"size" : len(c.users), "string" : profileString}
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

	# Calculates distance between communities

	commCount = len(communities)
	minSim = float("inf")
	maxSim = 0

	for i in range(1, commCount + 1):
	 	for j in range(i+1, commCount + 1):
	 		if i != j:
		 		link = {}
		 		link["source"] = i - 1
		 		link["target"] = j - 1
		 		commSim = clusterer.dbi2(communities[i-1],communities[j-1]);

		 		# Get minimum and maximum similarity values between communities
		 		if(commSim < minSim):
		 			minSim = commSim
		 		if(commSim > maxSim):
		 			maxSim = commSim

		 		linkVal = commSim
		 		# print("Similarity between", i, "and", j, ":", commSim)
		 		# linkVal = math.floor((commSim - 1) / 2 * 100) + 2;
		 		# if linkVal < 2:
		 		# 	linkVal = 2
		 		link["value"] = linkVal
		 		data["communityLinks"].append(link)

	if minSim == float("inf"):
		minSim = "Number.POSITIVE_INFINITY"
	if maxSim == float("inf"):
		maxSim = "Number.POSITIVE_INFINITY"

	data["minCommunitySimilarity"] = minSim
	data["maxCommunitySimilarity"] = maxSim

	print("\nFinished! Generated", len(communities), "communities")
	print("Modularity:", clusterer.modularity())
	# print("FPUPC:", clusterer.fpupc())

	print("\nWriting json...")
	with open('vis.json', 'w') as outfile:
	    json.dump(data, outfile)

	print("Writing tweet word cloud data...")
	with open('communitytweets.json', 'w') as outfile:
	    json.dump(communityTweets, outfile)

	print("Writing profile description word cloud data...")
	with open('communityprofile.json', 'w') as outfile:
	    json.dump(communityProfile, outfile)

	print("Writing community statistics...")
	with open('stats.json', 'w') as outfile:
	    json.dump(stats, outfile)

	countWords("communitytweets.json", "tweetWordCounts.json")
	countWords("communityprofile.json", "profileWordCounts.json")

	# print("Stats (Location):")
	# for commName, commLocs in stats["location"].items():
	# 	print("\tCommunity " + str(commName))
	# 	for loc, count in commLocs.items():
	# 		print("\t\t" + str(count) + " in " + loc)

	output = {}
	output['mod'] = math.ceil(clusterer.modularity()*1000)/1000
	output['algo'] = getAlgoString(algoVal, k)
	output['param'] = getParamString(paramVal)
	output['measure'] = getMeasureString(measureVal)
	output['dbi'] = math.ceil(clusterer.dbi() * 1000) / 1000
	if output['dbi'] == -1:
		output['dbi'] = 'N/A'

	return output