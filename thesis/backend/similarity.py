from .model import *
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

	def createOutgoingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and userList[u].id in user.following.keys():
				edges[u] = 1
		return edges

	def createIncomingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and user.id in userList[u].following.keys():
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

	def totalHashtags(self, user):
		total = 0
		for h in user.hashtags:
			total += user.hashtags[h]
		return total

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
			total1 = self.totalHashtags(user1)
			total2 = self.totalHashtags(user2)
			val = (1 - abs(user1.hashtags[k]/total1 - user2.hashtags[k]/total2))
			val *= ((user1.hashtags[k]+user2.hashtags[k]) / (total1+total2))
			sim += val
		return sim

	def createOutgoingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and len(self.commonHashtags(user, userList[u]))>0:
				edges[u] = 1
		return edges

	def createIncomingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and len(self.commonHashtags(user, userList[u]))>0:
				edges[u] = 1
		return edges

class Retweets(Parameter):
	"""This class represents the hashtag similarity parameter"""

	def __init__(self):
		Parameter.__init__(self)

	def commonRetweets(self, user1, user2):
		retweets = []
		for r in user1.retweets:
			if r in user2.retweets.keys():
				retweets.append(r)
		return retweets

	"""Computes for retweeting similarity
	Parameter:
	user1 - first user
	user2 - second user
	"""
	def similarity(self,user1,user2):
		a = len(self.commonRetweets(user1, user2))
		b1 = 0
		if user2.id in user1.retweets:
			b1 = user1.retweets[user2.id]
		b2 = 0
		if user1.id in user2.retweets:
			b2 = user2.retweets[user1.id]
		b = b1+b2
		if len(user1.retweets)==0 or len(user2.retweets)==0:
			a = 0
			b = 0
		else:
			a /= math.sqrt(len(user1.retweets))*math.sqrt(len(user2.retweets))
			b /= len(user1.retweets)*len(user2.retweets)
		return a+b

	def createOutgoingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and userList[u].id in user.retweets.keys():
				edges[u] = 1
		return edges

	def createIncomingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and user.id in userList[u].retweets.keys():
				edges[u] = 1
		return edges