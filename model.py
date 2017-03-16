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
		print("Deleted", len(toDelete), " users")

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

class Algorithm:
	"""This class represents an abstract algorithm"""

	"""Basic constructor for an algorithm
	Parameter:
	parameter - similarity parameter to use for this algorithm
	"""
	def __init__(self,parameter):
		self.parameter = parameter

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
	def run(self,user1,user2):
		raise NotImplementedError

	"""Takes a list of users and returns a user that represents the average of
	all the users according to the parameter

	Parameter:
	users - users to average

	Returns:
	average of all users
	"""
	def average(self,users):
		raise NotImplementedError

	"""Returns the modularity given a list of communities
		
	Parameter:
	communities - list of communities

	Returns:
	modularity of these communities (floating point)
	"""
	def modularity(self, communities):
		raise NotImplementedError

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