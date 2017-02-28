from LoadUserFriendships import *
from model import *
from similarity import *
import random

class KMeans(Algorithm):

	def run(self, users):
		numClusters = 2 # For now this is hardcoded

		userIds = list(users.keys()) # Create list of user ideas
		indices = random.sample(range(0, len(users)), numClusters) # Randomize centroids for each cluster (returns indices in userIds list)
		centroids = [] # Initialize array of centroids
		userClusters = {} # Initialize dictionary of user clusters (maps user ids to their clusters)
		prevUserClusters = {} # Initialize dictionary of previous user clusters (copy of previous iteration's user clusters)
		clusters = {} # Maps cluster centroids to dictionaries of users in the cluster

		iterationCount = 1 # Initialize iteration count to 1

		print("\nInitial Centroids:")

		# Add randomly selected centroids to centroids array
		for i in indices:
			centroids.append(users[userIds[i]])
			print("-", usernames[centroids[len(centroids)-1].id])
		
		# Assign users to clusters with closest centroids until clusters don't change
		while True:
			clusters = {}
			prevUserClusters = userClusters.copy() # Copy current set of user clusters to previous set of user clusters

			# Empty clusters
			for c in centroids:
				clusters.update({c.id: {}})

			# Assign users to more similar centroids
			for u in users.values():
				closestCentroid = None
				maxSimilarity = None

				# Compare with every centroid
				for c in centroids:
					currSimilarity = self.parameter.similarity(c, u) # Check similarity between current centroid and current user
					print(c.id, u.id, currSimilarity)

					# Set closest centroid of user if so far current centroid is the most similar
					if closestCentroid is None or currSimilarity > maxSimilarity:
						closestCentroid = c.id
						maxSimilarity = currSimilarity

				# Once closest centroid to user is found, update lists
				clusters[closestCentroid].update({u.id: u})
				userClusters[u.id] = closestCentroid
				# print("closestCentroid:", closestCentroid)

			end = True

			# Check if user clusters are the same as in the previous iteration
			for uc in userClusters.keys():
				if uc in prevUserClusters:
					if not prevUserClusters[uc] == userClusters[uc]: # If current user's cluster was different in the previous iteration, clusters aren't final
						end = False
				else: # If the user doesn't even exist in the prevUserClusters (NOTE: Not actually sure how this would happen), clusters aren't final
					end = False

			# print("userClusters:", userClusters)
			# print("prevUserClusters:", prevUserClusters)

			# Break out of loop if clusters are final
			if end:
				break

			newCentroids = []

			# Set new centroids for next iteration
			for c in centroids:
				averageUser = self.parameter.average(clusters[c.id]) # Generate the average user for the cluster of the given centroid
				averageUser.id = c.id # Assign the ID of the generated user (so it doesn't repeat)
				newCentroids.append(averageUser) # Add the generated user to the new list of centroids

			centroids = newCentroids # Set new centroids as current centroids

			print("\nIteration:", iterationCount)
			iterationCount += 1

		communities = []

		print("\nStopped at iteration #", iterationCount)

		# Convert clusters to communities
		for key, value in clusters.items():
			communities.append(value)

		# Return the generated communities
		return communities

# For running the code; not important once we have a proper implementation

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