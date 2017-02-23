from Model import *
from Loader import *
from Similarity import *
from KMeans import *

loader = Loader("MongoDB Tweet Data/", "user.json", "following.json")
following = Following()
kmeans = KMeans(following)
clusterer = Clusterer(loader, kmeans)
clusterer.run()
communities = clusterer.communities

commNum = 1

for c in communities:
	print("\nCommunity #", commNum)
	commNum += 1

	for u in c.users:
		print("-", u.id)

print("Finished!")
print("Modularity:", clusterer.modularity())
print("FPUPC:", clusterer.fpupc())