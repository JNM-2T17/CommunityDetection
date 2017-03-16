from model import *
from similarity import *
from collections import *
import random

class KMeans(Algorithm):
	def __init__(self, parameter, k):
		self.k = k
		super(KMeans, self).__init__(parameter)

	def run(self, users):
		numClusters = self.k # For now this is hardcoded

		# If there are less users than clusters that need to be formed
		if len(users) < numClusters:
			print("LESS USERS THAN CLUSTERS:", len(users), " < ", numClusters)
			communities = []

			# Form a community for each user
			for key, value in users.items():
				c = Community()
				c.addUser(value)
				communities.append(c)

			print("numClusters = " + str(numClusters) + ", community count = " + str(len(communities)))

		# If there are at least as many users as clusters that need to be formed
		else:
			print("MORE OR EQUAL USERS THAN CLUSTERS")
			userIds = list(users.keys()) # Create list of user ideas
			indices = random.sample(range(0, len(users)), numClusters) # Randomize centroids for each cluster (returns indices in userIds list)
			centroids = [] # Initialize array of centroids
			userClusters = {} # Initialize dictionary of user clusters (maps user ids to their clusters)
			prevUserClusters = {} # Initialize dictionary of previous user clusters (copy of previous iteration's user clusters)
			clusters = {} # Maps cluster centroids to dictionaries of users in the cluster

			iterationCount = 1 # Initialize iteration count to 1

			# Add randomly selected centroids to centroids array
			for i in indices:
				centroids.append(users[userIds[i]])
			
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
						# print(c.id, u.id, currSimilarity)

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
				c = Community()
				for k,v in value.items():
					c.addUser(v)
				if c.len() > 0:
					communities.append(c)

		# Append blank communities to make up for difference in number of users and required clusters
		for i in range(0, numClusters - len(communities)):
			communities.append(Community())

		# Return the generated communities
		return communities

class DivisiveHC(Algorithm):

	def run(self, users):
		com = Community()
		userids = list(users.keys())
		for id in userids:
			com.addUser(users[id])

		current = [com]
		frontier = deque()
		frontier.append(com)
		prevmod = self.parameter.modularity(current)

		iterCount = 0
		# while there are communities to split

		while frontier:
			iterCount+=1
			print("Iteration", iterCount)
			# get first community and split
			temp = frontier.popleft()
			kmeans = KMeans(self.parameter, 2)

			userDict = {}
			for u in temp.users:
				userDict[u.id] = u
			results = kmeans.run(userDict)

			t1 = results[0]
			t2 = results[1]

			# replace previous community with halves
			current.remove(temp)

			current.append(t1)
			current.append(t2)

			# get modularity
			mod = self.parameter.modularity(current)
			print("New mod =", mod, ", prev mod =", prevmod)
			# if splitting worsened modularity
			if mod < prevmod:
				print(mod, prevmod)
				# remove new divisions and restore old whole
				current.pop()
				current.pop()
				current.append(temp)
			else:	 # if splitting improved modularity
				
				# if halves have more than one element, add to frontier
				if t1.len() > 0:
					frontier.append(t1)
				
				if t2.len() > 0:
					frontier.append(t2)

				# update modularity
				prevmod = mod

		return current

# For running the code; not important once we have a proper implementation

# usernames = {}
# with open("Dummy Tweet Data/TestUsernames.csv", 'r') as f:
# 	r = csv.reader(f);
# 	for row in r:
# 		if len(row)>=1:
# 			usernames[row[0]] = row[1]

# loadedUsers = load_user_friendships("Dummy Tweet Data", "/TestUsersList.csv", "/TestFFIds.csv")
# following = Following()
# kmeans = KMeans(following)
# communities = kmeans.run(loadedUsers)

# commNum = 1

# for c in communities:
# 	print("\nCommunity #", commNum)
# 	commNum += 1

# 	for u in c.keys():
# 		print("-", usernames[u])