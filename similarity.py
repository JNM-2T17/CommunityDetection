from model import *
import math

class Following(Parameter):
	"""This class represents the following similarity parameter"""

	def __init__(self):
		Parameter.__init__(self)

	"""Computes for following similarity
	Parameter:
	user1 - first user
	user2 - second user
	"""
	def similarity(self,user1,user2):
		cFriend = 0
		for k, v in user1.following.items():
			if k in user2.following:
				cFriend += 1

		cFollowers = 0
		for k, v in user1.followers.items():
			if k in user2.followers:
				cFollowers += 1

		friendDenom = math.sqrt(len(user1.following) * len(user2.following))
		followDenom = math.sqrt(len(user1.followers) * len(user2.followers))

		if friendDenom == 0 and followDenom == 0:
			return 0

		elif friendDenom == 0:
			return cFollowers / followDenom

		elif followDenom == 0:
			return cFriend / friendDenom

		else:
			return (cFriend / friendDenom + cFollowers / followDenom) 

	"""Takes a list of users and returns a user that represents the average of
	all the users according to the parameter

	Parameter:
	users - users to average

	Returns:
	average of all users
	"""
	def average(self,users):
		followingCount = {}
		followersCount = {}

		for u in users.values():
			for userId in u.following.keys():
				if userId in followingCount:
					followingCount[userId] += 1
				else:
					followingCount[userId] = 1
			for userId in u.followers.keys():
				if userId in followersCount:
					followersCount[userId] += 1
				else:
					followersCount[userId] = 1

		numUsers = len(users)

		averageFollowing = {}
		# print(users)

		for userId, count in followingCount.items():
			if count*1.0/numUsers >= 0: # Change this from 0
				if not userId in users:
					dummyUser = User(userId)
					averageFollowing[userId] = dummyUser
				else:
					averageFollowing[userId] = users[userId]

		averageFollowers = {}

		for userId, count in followersCount.items():
			if count*1.0/numUsers >= 0: # Change this from 0
				if not userId in users:
					dummyUser = User(userId)
					averageFollowers[userId] = dummyUser
				else:
					averageFollowers[userId] = users[userId]

		averageUser = User("Average")
		averageUser.following = averageFollowing
		averageUser.followers = averageFollowers

		# print(averageUser.id, "\nFollowing:", averageUser.following, "\nFollowers:", averageUser.followers)

		return averageUser

	"""Returns the modularity of the generated communities"""
	def modularity(self, communities):
		print("Calculating Modularity")
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
							a = 1.0 if j.id in i.following else 0.0
							a -= (len(i.outgoingEdges))*(len(j.outgoingEdges))/(2.0*m)
							q += a
			q /= 2.0*m
			print("Modularity =", q)
			return q

	def createEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and userList[u].id in user.following.keys():
				edges[u] = 1
		return edges

class Hashtags(Parameter):
	"""This class represents the hashtag similarity parameter"""

	def __init__(self):
		Parameter.__init__(self)

	def commonHashtags(self, u1, u2):
		commonHashtags = []
		u2keys = u2.hashtags.keys()
		for i in u1.hashtags:
			if i in u2keys:
				commonHashtags.append(i)
		return commonHashtags

	"""Computes for hashtag similarity
	Parameter:
	user1 - first user
	user2 - second user
	"""
	def similarity(self,user1,user2):
		c = self.commonHashtags(user1, user2)
		n = len(c)
		sim = 0
		for k in c:
			val = (1 - abs(user1.hashtags[k]/len(user1.hashtags) - user2.hashtags[k]/len(user2.hashtags)))
			val *= ((user1.hashtags[k]+user2.hashtags[k]) / (len(user1.hashtags)+len(user2.hashtags)))
			sim += val
		return sim

	"""Takes a list of users and returns a user that represents the average of
	all the users according to the parameter

	Parameter:
	users - users to average

	Returns:
	average of all users
	"""
	def average(self,users):
		hashtagCount = {}

		for u in users.values():
			for h in u.hashtags.keys():
				if h in hashtagCount:
					hashtagCount[h] += 1
				else:
					hashtagCount[h] = 1

		numUsers = len(users)

		averageHashtags = {}

		for hashtag, count in hashtagCount.items():
			if count*1.0/numUsers >= 0.4: # Change this from 0
				averageHashtags[hashtag] = math.ceil(count*1.0/numUsers)

		averageUser = User("Average")
		averageUser.hashtags = averageHashtags 

		print("Average User:", len(averageUser.hashtags));

		return averageUser

	"""Returns the modularity of the generated communities"""
	def modularity(self, communities):
		print("Calculating Modularity")
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
							a = 1.0 if j.id in i.following else 0.0
							a -= (len(i.outgoingEdges))*(len(j.outgoingEdges))/(2.0*m)
							q += a
			q /= 2.0*m
			print("Modularity =", q)
			return q

	def createEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and len(self.commonHashtags(user, userList[u]))>0:
				edges[u] = 1
		return edges