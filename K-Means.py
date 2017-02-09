from LoadUserFriendships import *
from Model import *
from Similarity import *
import random

class KMeans(Algorithm):

	def run(self, users):
		numClusters = 2 # What value do we set this to?

		userIds = list(users.keys())
		indices = random.sample(range(0, len(users)), numClusters)
		centroids = []
		userClusters = {}
		prevUserClusters = {}
		clusters = {}

		iterationCount = 1

		print("\nInitial Centroids:")

		for i in indices:
			centroids.append(users[userIds[i]])
			print("-", usernames[centroids[len(centroids)-1].id])
		
		while True:
			clusters = {}
			prevUserClusters = userClusters.copy()

			for c in centroids:
				clusters.update({c.id: {}})

			for u in users.values():
				closestCentroid = None
				maxSimilarity = None

				for c in centroids:
					currSimilarity = self.parameter.similarity(c, u)
					print(c.id, u.id, currSimilarity)

					if closestCentroid is None or currSimilarity > maxSimilarity:
						closestCentroid = c.id
						maxSimilarity = currSimilarity

				clusters[closestCentroid].update({u.id: u})
				userClusters[u.id] = closestCentroid
				# print("closestCentroid:", closestCentroid)

			end = True

			for uc in userClusters.keys():
				if uc in prevUserClusters or uc in userClusters:
					if not uc in prevUserClusters or not uc in userClusters:
						end = False
					elif not prevUserClusters[uc] == userClusters[uc]:
						end = False

			# print("userClusters:", userClusters)
			# print("prevUserClusters:", prevUserClusters)

			if end:
				break
				

			newCentroids = []

			for c in centroids:
				averageUser = self.parameter.average(clusters[c.id])
				averageUser.id = c.id
				newCentroids.append(averageUser)

			centroids = newCentroids

			print("\nIteration:", iterationCount)
			iterationCount += 1

		communities = []

		print("\nStopped at iteration #", iterationCount)

		for key, value in clusters.items():
			communities.append(value)

		return communities

usernames = {}
with open("Dummy Tweet Data/TestUsernames.csv", 'r') as f:
	r = csv.reader(f);
	for row in r:
		if len(row)>=1:
			usernames[row[0]] = row[1]

loadedUsers = load_user_friendships("Dummy Tweet Data", "/TestUsersList.csv", "/TestFFIds.csv")
following = Following()
kmeans = KMeans(following)
communities = kmeans.run(loadedUsers)

commNum = 1

for c in communities:
	print("\nCommunity #", commNum)
	commNum += 1

	for u in c.keys():
		print("-", usernames[u])