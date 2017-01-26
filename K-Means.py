class K-Means(Algorithm):

	def centroidsAreEqual(centroids1, centroids2):
		raise NotImplementedError

	def run(users):
		numClusters = 3 # What value do we set this to?

		indices = random.sample(range(0, len(users)), numClusters)
		centroids = []
		userClusters = {}
		prevUserClusters = {}
		clusters = {}

		for i in indices:
			centroids.append(users[i])
		
		while True:
			clusters = {}
			prevUserClusters = userClusters.copy()

			for c in centroids:
				clusters.update({c.id: []})

			for u in users.values():
				closestCentroid = None
				maxSimilarity = None

				for c in centroids:
					currSimilarity = parameter.similarity(c, u)
					if closestCentroid is None or currSimilarity > maxSimilarity:
						closestCentroid = c.id
						maxSimilarity = currSimilarity

				clusters[closestCentroid].append(v)
				userClusters[u.id] = c.id

			newCentroids = []
			centroidNum = 0

			for uc in userClusters.keys():
				if not prevUserClusters[uc] == userClusters[uc]:
					break

			for c in centroids:
				averageUser = parameter.average(clusters[c.id])
				averageUser.id = c.id
				newCentroids.append(averageUser)

			else:
				centroids = newCentroids

		communities = []

		for key, value in clusters:
			communities.append(value)

		return communities