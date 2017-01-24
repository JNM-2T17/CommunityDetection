class K-Means(Algorithm):

	def centroidsAreEqual(centroids1, centroids2):
		raise NotImplementedError

	def run(users):
		numClusters = 3 # What value do we set this to?

		indices = random.sample(range(0, len(users)), numClusters)
		centroids = []

		for i in indices:
			centroids.append(users[i])
		
		while True:
			clusters = {}

			for c in centroids:
				clusters.update({c.id: []})

			for u in users:
				closestCentroid = None
				maxSimilarity = None

				for c in centroids:
					currSimilarity = parameter.similarity(c, u)
					if closestCentroid is None or currSimilarity > maxSimilarity:
						closestCentroid = c.id
						maxSimilarity = currSimilarity

				clusters[closestCentroid].append(v)

			newCentroids = []
			centroidNum = 0

			for c in centroids:
				averageUser = parameter.average(clusters[c.id])
				averageUser.id = centroidNum
				newCentroids.append(averageUser)
				centroidNum += 1

			if centroidsAreEqual(centroids, newCentroids):
				break

			else:
				centroids = newCentroids

		communities = []

		for key, value in clusters:
			communities.append(value)

		return communities