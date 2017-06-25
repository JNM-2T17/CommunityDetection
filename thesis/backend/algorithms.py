from .model import *
from .similarity import *
from collections import *
import random

MAX_DIST = 0
MIN_DIST = 1
AVE_DIST = 2

class KMeans(Algorithm):
	def __init__(self, parameter, k = None):
		if k is None:
			self.hasSetClusterCount = False
		else:
			self.k = k
			self.hasSetClusterCount = True
		super(KMeans, self).__init__(parameter)

	def run(self, users):
		global MAX_DIST
		global MIN_DIST
		global AVE_DIST

		if self.hasSetClusterCount:
			numClusters = self.k
		else:
			numClusters = 1
			
		while True:
			# If there are less users than clusters that need to be formed
			if len(users) < numClusters:
				communities = []

				# Form a community for each user
				for key, value in users.items():
					c = Community()
					c.addUser(value)
					communities.append(c)

				# print("numClusters = " + str(numClusters) + ", community count = " + str(len(communities)))

			# If there are at least as many users as clusters that need to be formed
			else:
				userIds = list(users.keys()) # Create list of user ideas
				indices = random.sample(range(0, len(users)), numClusters) # Randomize centroids for each cluster (returns indices in userIds list)
				centroids = [] # Initialize array of centroids
				prevUserClusters = {} # Initialize dictionary of previous user clusters (copy of previous iteration's user clusters)
				clusters = {} # Maps cluster centroids to dictionaries of users in the cluster

				iterationCount = 1 # Initialize iteration count to 1

				mode = AVE_DIST
				
				clusters = [[] for i in range(0,numClusters)]
				ctr = 0
				# Add randomly selected centroids to clusters array
				for i in indices:
					clusters[ctr].append(users[userIds[i]])
					ctr += 1
				
				for u in users.values():
					u.prevGrp = -1
					u.currGrp = -1
				
				end = False
				# Assign users to clusters with closest centroids until clusters don't change
				while not end:
					prevUserClusters = clusters.copy() # Copy current set of user clusters to previous set of user clusters
					clusters = [[] for i in range(0,numClusters)]
				
					# Assign users to more similar centroids
					for u in users.values():
						closestCentroid = None
						similarity = None
						ctr2 = 0
						temp = [0 for i in range(0,numClusters)]
							
						for com in prevUserClusters:
							sim = None

							currSim = -1
							for v in com:
								currSim = self.parameter.similarity(u,v)
								if mode == MAX_DIST:
									if sim is None:
										if abs(currSim) < 1e-4:
											sim = currSim
									if abs(currSim) < 1e-4 and currSim < sim:
										sim = currSim
								elif mode == MIN_DIST:
									if sim is None:
										if abs(currSim - 1) < 1e-4:
											sim = currSim
									if abs(currSim - 1) < 1e-4 and currSim > sim:
										sim = currSim
								elif mode == AVE_DIST:
									if sim is None:
										sim = float(currSim) / len(com)
									else:
										sim += float(currSim) / len(com)

							if sim is None:
								sim = 0

							if closestCentroid is None or sim > similarity:
								closestCentroid = ctr2
								similarity = sim

							temp[ctr2] = sim
							ctr2 += 1
							#print(u.id,temp)

						# Once closest centroid to user is found, update lists
						clusters[closestCentroid].append(u)
						u.currGrp = closestCentroid
						# print("closestCentroid:", closestCentroid)

					end = True

					# Check if user clusters are the same as in the previous iteration
					for u in users.values():
						# print(u.id,u.prevGrp,u.currGrp)
						if u.prevGrp != u.currGrp:
							end = False
						u.prevGrp = u.currGrp

					# print("userClusters:", userClusters)
					# print("prevUserClusters:", prevUserClusters)

					# Break out of loop if clusters are final
					if end:
						break

					# print("\nIteration:", iterationCount)
					iterationCount += 1

				communities = []

				# print("\nStopped at iteration #", iterationCount)

				# Convert clusters to communities
				for value in clusters:
					c = Community()
					for v in value:
						c.addUser(v)
					if c.len() > 0:
						communities.append(c)

			if self.hasSetClusterCount:
				break

			else:
				currModularity = self.parameter.modularity(communities)

				if numClusters > 1:
					if currModularity < prevModularity:
						communities = prevCommunities
						numClusters -= 1
						break

				prevCommunities = communities
				prevModularity = currModularity
				numClusters += 1

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
			# print("Iteration", iterCount)
			# get first community and split
			temp = frontier.popleft()
			kmeans = KMeans(self.parameter, 2)

			userDict = {}
			for u in temp.users:
				userDict[u.id] = u

			ctr = 0
			found = False
			while ctr < 5:
				results = kmeans.run(userDict)
				t1 = results[0]
				t2 = results[1]

				# replace previous community with halves
				current.remove(temp)

				current.append(t1)
				current.append(t2)

				# get modularity
				mod = self.parameter.modularity(current)
				if mod>prevmod:
					found = True
					break
				else:
					# remove new divisions and restore old whole
					current.pop()
					current.pop()
					current.append(temp)
				ctr += 1
			# print(len(current),"communities")
			# print("New mod =", mod, ", prev mod =", prevmod)
			# if splitting worsened modularity
			if found:
				# if halves have more than one element, add to frontier
				if t1.len() > 1:
					frontier.append(t1)
				
				if t2.len() > 1:
					frontier.append(t2)

				# update modularity
				prevmod = mod

		return current