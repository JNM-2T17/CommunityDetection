import math

class Tweet:
	"""This class represents a tweet."""

	"""basic constructor for a tweet
	Parameters:
	tweetdata - json information of tweet
	"""
	def __init__(self,tweetdata):
		self.tweetdata = tweetdata


class User:
	"""This class represents a user in the dataset."""

	"""Basic constructor for User
	Parameter:
	id - id of anonymized user
	"""
	def __init__(self,id):
		self.id = id
		self.following = {}
		self.followers = {}
		self.tweets = []
		self.hashtags = {}
		self.retweets = {}
		self.mentions = {}
		self.outgoingEdges = {}
		self.incomingEdges = {}

	"""adds a user to this user's following list
	Parameter:
	user - user to follow
	"""
	def follow(self,user):
		self.following[user.id] = user
		user.followers[self.id] = self

	def saveJson(self, json):
		self.data = json
	
	def countNetworkSize(self):
		return len(self.outgoingEdges) + len(self.incomingEdges)

	"""posts a tweet from this user
	Parameter:
	post - post to add
	"""
	def post(self,post):
		self.tweets.append(post)

	"""This method returns the term frequency matrix of this user
	"""
	def termFrequency(self):
		raise NotImplementedError

class Clusterer:
	"""This class takes users and algorithm and then performs community 
	detection on the users using the given algorithm
	"""

	"""Basic constructor for a clusterer
	Parameters:
	users - users to perform community detection on
	algorithm - algorithm to use. Note: algorithm must have a similarity 
				parameter set
	"""
	def __init__(self,loader,algorithm):
		self.loader = loader
		self.users = loader.load_user_friendships()
		self.algorithm = algorithm
		self.communities = []
		for user in self.users:
			self.users[user].outgoingEdges = algorithm.parameter.createOutgoingEdges(self.users[user], self.users)
			self.users[user].incomingEdges = algorithm.parameter.createIncomingEdges(self.users[user], self.users)
		toDelete = []
		for i in self.users:
			if self.users[i].countNetworkSize() == 0:
				toDelete.append(i)
		for i in toDelete:
			del self.users[i]
		print("Deleted", len(toDelete), "users")

	"""Runs the algorithm on the users
	"""
	def run(self):
		self.communities = self.algorithm.run(self.users)

	"""Returns the fpupc of the generated communities"""
	def fpupc(self):
		if len(self.communities) == 0:
			return 0
		else:
			total = 0.0
			for x in self.communities:
				total += x.fpu()
			total /= len(self.communities)
			return total

	"""Returns the modularity of the generated communities"""
	def modularity(self):
		return self.algorithm.parameter.modularity(self.communities)

	"""Returns the Davies-Bouldin Index
	Parameters:
	communities - list of communities to evaluate
	Returns:
	DBI of communities
	"""
	def dbi(self):
		return self.algorithm.parameter.dbi(self.communities)	

	"""Returns the Davies-Bouldin Index between Two Communities
	Parameters:
	comm1 - index of first community
	comm2 - index of second community
	Returns:
	DBI of communities
	"""
	def dbi2(self, comm1, comm2):
		dist = 0

		for u in comm1.users:
			for v in comm2.users:
				dist += 1 - self.algorithm.parameter.similarity(u,v)

		dist /= len(comm1.users) * len(comm2.users)

		return dist	

	def cleanCommunities(self):
		indices = []
		for i in range(0, len(self.communities)):
			if len(self.communities[i].users) == 0:
				indices.append(i)
		for i in range(len(indices)-1, -1, -1):
			print(i)
			self.communities.pop(indices[i])	

class Algorithm:
	"""This class represents an abstract algorithm"""

	"""Basic constructor for an algorithm
	Parameter:
	parameter - similarity parameter to use for this algorithm
	"""
	def __init__(self,parameter,cosine=False):
		self.parameter = parameter
		self.cosine = cosine

	"""Runs this algorithm on the given users
	Parameter:
	users - users to run algorithm on
	"""
	def run(self,users):
		raise NotImplementedError

class Parameter:
	"""This class represents an abstract parameter"""

	"""Basic constructor for an Parameter
	"""
	def __init__(self):
		pass

	"""checks the similarity between two users
	Parameter:
	user1 - first user
	user2 - second user
	"""
	def similarity(self,user1,user2,cosine=False):
		if cosine:
			return self.cosine(user1,user2)
		else:
			return self.zhangSimilarity(user1,user2)

	"""Returns the similarity of the two users using this similarity parameter 
	according to Zhang, 2012
	Parameters:
	user1 - first user
	user2 - second user
	"""
	def zhangSimilarity(self,user1,user2):
		raise NotImplementedError

	"""Returns the cosine similarity of the two users using this similarity 
	parameter
	Parameters:
	user1 - first user
	user2 - second user
	"""
	def cosine(self,user1,user2):
		raise NotImplementedError

	"""Returns the modularity given a list of communities
		
	Parameter:
	communities - list of communities

	Returns:
	modularity of these communities (floating point)
	"""
	def modularity(self, communities):
		if len(communities) == 0:
			return 1
		else:
			m = 0
			for c in communities:
				total = 0
				for x in c.users:
					total += len(x.outgoingEdges)
				m += total
			q = 0
			for community in communities:
				for i in community.users:
					for j in community.users:
						if i != j:
							a = 1.0 if j.id in i.outgoingEdges.keys() or j.id in i.incomingEdges.keys() else 0.0
							a -= (len(i.outgoingEdges))*(len(j.outgoingEdges))/(2.0*m)
							q += a
			q /= 2.0*m
			# print("Modularity =", q)
			return q

	"""Returns the Davies-Bouldin Index
	Parameters:
	communities - list of communities to evaluate
	Returns:
	DBI of communities
	"""
	def dbi(self,communities):
		sI = [0 for i in range(0,len(communities))]
		mIJ = [[0 for i in range(0,len(communities))] for j in range(0,len(communities))]
		
		for i in range(0,len(communities)):
			sI[i] = 0
			currCom = communities[i]
			for user in currCom.users:
				sim = 0
				for user2 in currCom.users:
					sim += 1 - self.similarity(user,user2)
				sim /= len(currCom.users)
				sI[i] += sim ** 2
			sI[i] = math.sqrt(sI[i] / len(currCom.users))

			for j in range(i,len(communities)):
				if i == j:
					mIJ[i][j] = 0
				else:
					mIJ[i][j] = 0;
					com2 = communities[j]
					for user1 in currCom.users:
						for user2 in com2.users:
							mIJ[i][j] += 1 - self.similarity(user1,user2)

					mIJ[i][j] /= len(currCom.users) * len(com2.users)
				mIJ[j][i] = mIJ[i][j]

		dbiVal = 0
		for i in range(0,len(communities)):
			maxM = -1;
			for j in range(0,len(communities)):
				if i != j:
					r = (sI[i] + sI[j]) / mIJ[i][j]
					if r > maxM:
						maxM = r
			dbiVal += maxM
		return dbiVal / len(communities)

	"""Returns the dictionary of outgoing edges {userId: weight} given a user and the list of users
		
	Parameter:
	user - user to generate edges
	userList - list of users

	Returns:
	dictionary of outgoing edges
	"""
	def createOutgoingEdges(self, user, userList):
		raise NotImplementedError

	"""Returns the dictionary of incoming edges {userId: weight} given a user and the list of users
		
	Parameter:
	user - user to generate edges
	userList - list of users

	Returns:
	dictionary of incoming edges
	"""
	def createIncomingEdges(self, user, userList):
		raise NotImplementedError

class Community:
	"""This class represents a detected cluster of users i.e. a community."""

	"""Basic constructor for community
	"""
	def __init__(self):
		self.users = []

	"""Adds a user to this community
	Parameter:
	user - user to add
	"""
	def addUser(self,user):
		self.users.append(user)

	"""Computes the average mutual following links per user in this community.
	Returns:
	The average mutual following links per user in this community.
	"""
	def fpu(self):
		if len(self.users) == 0:
			return 0
		total = 0.0
		for x in self.users:
			temp = 0.0
			for k,v in x.following.items():
				if v in self.users and x.id in v.following:
					temp += 1
			total += temp
		total /= len(self.users)
		return total

	def len(self):
		return len(self.users)