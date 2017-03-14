# Implementation of K-means without thinking about the communities yet

import random

def displayClusters(clusters):
	for key, value in clusters.items():
		print(key, ":", value)

def getDistance(value1, value2): # For now it only deals with 1-dimensional distance; to change it to euclidian distance I have to change some stuff in the main code too haha
	return abs(value1 - value2)

def arraysAreEqual(array1, array2):
	if not len(array1) == len(array2):
		return False

	else:
		for i in range(0, len(array1)):
			if not array1[i] == array2[i]:
				return False

		return True

def kMeans(numClusters, values):
	indices = random.sample(range(0, len(values)), numClusters)
	centroids = []
	iterationCount = 1

	for i in indices:
		centroids.append(values[i])
	
	while True:
		clusters = {}

		for c in centroids:
			clusters.update({c: []})

		for v in values:
			closestCentroid = None
			minDistance = None

			for c in centroids:
				currDistance = getDistance(c, v)
				if closestCentroid is None or currDistance < minDistance:
					closestCentroid = c
					minDistance = currDistance

			clusters[closestCentroid].append(v)

		newCentroids = []

		for c in centroids:
			clusterValues = clusters[c]
			newCentroids.append(sum(clusterValues) / float(len(clusterValues)))

		if arraysAreEqual(centroids, newCentroids):
			break

		else:
			centroids = newCentroids

		print("\nIteration", iterationCount)
		displayClusters(clusters)
		iterationCount += 1

	print("\nIteration", iterationCount, "(FINAL)")
	displayClusters(clusters)
	return clusters

values = [0, 1, 2, 9, 10, 11, 12, 13]
kMeans(2, values)