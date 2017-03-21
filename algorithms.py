from model import *
from similarity import *
from collections import *
import random

MIN_DIST = 0
MAX_DIST = 1
AVE_DIST = 2

class KMeans(Algorithm):
	def __init__(self, parameter, k):
		self.k = k
		super(KMeans, self).__init__(parameter)

	def run(self, users):
		global MIN_DIST
		global MAX_DIST
		global AVE_DIST
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
			prevUserClusters = {} # Initialize dictionary of previous user clusters (copy of previous iteration's user clusters)
			clusters = {} # Maps cluster centroids to dictionaries of users in the cluster

			iterationCount = 1 # Initialize iteration count to 1


			mode = MAX_DIST
			
			clusters = [[] for i in range(0,self.k)]
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
				
				# Assign users to more similar centroids
				for u in users.values():
					closestCentroid = None
					similarity = None
					ctr2 = 0
						
					for com in prevUserClusters:
						if mode == MIN_DIST:
							sim = 2 ** 31 - 1
						elif mode == MAX_DIST:
							sim = -1
						elif mode == AVE_DIST:
							sim = None

						currSim = -1
						for v in com:
							currSim = self.parameter.similarity(u,v)
							if mode == MIN_DIST:
								if currSim != 0 and currSim < sim:
									sim = currSim
							elif mode == MAX_DIST:
								if currSim > sim:
									sim = currSim
							elif mode == AVE_DIST:
								if sim == None:
									sim = float(currSim) / len(com)
								else:
									sim += float(currSim) / len(com)

						if mode == MIN_DIST and sim == 2 ** 31 - 1:
							sim = 0

						if closestCentroid is None or sim < similarity:
							closestCentroid = ctr2
							similarity = sim

						ctr2 += 1

					# Once closest centroid to user is found, update lists
					clusters[closestCentroid].append(u)
					u.currGrp = closestCentroid
					# print("closestCentroid:", closestCentroid)

				end = True

				# Check if user clusters are the same as in the previous iteration
				for u in users.values():
					#print(u.id,u.prevGrp,u.currGrp)
					if u.prevGrp != u.currGrp:
						end = False
					u.prevGrp = u.currGrp

				# print("userClusters:", userClusters)
				# print("prevUserClusters:", prevUserClusters)

				# Break out of loop if clusters are final
				if end:
					break

				print("\nIteration:", iterationCount)
				iterationCount += 1

			communities = []

			print("\nStopped at iteration #", iterationCount)

			# Convert clusters to communities
			for value in clusters:
				c = Community()
				for v in value:
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
				if t1.len() > 1:
					frontier.append(t1)
				
				if t2.len() > 1:
					frontier.append(t2)

				# update modularity
				prevmod = mod

		return current