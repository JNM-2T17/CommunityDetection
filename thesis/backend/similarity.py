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
	def zhangSimilarity(self,user1,user2):
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

	"""Returns the cosine similarity of the two users using this similarity parameter
	Parameters:
	user1 - first user
	user2 - second user
	"""
	def cosine(self,user1,user2):
		userFollowing = []
		userFollowers = []
		for u in user1.following.keys():
			if u not in userFollowing:
				userFollowing.append(u)
		for u in user2.following.keys():
			if u not in userFollowing:
				userFollowing.append(u)

		cosineFollowingNum = 0
		cosineFollowingDen1 = 0
		cosineFollowingDen2 = 0

		for u in userFollowing:
			if u in user1.following and u in user2.following:
				cosineFollowingNum += 1
			if u in user1.following:
				cosineFollowingDen1 += 1
			if u in user2.following:
				cosineFollowingDen2 += 1

		cosineFollowing = cosineFollowingNum / math.sqrt(cosineFollowingDen1 * cosineFollowingDen2)

		for u in user1.followers.keys():
			if u not in userFollowers:
				userFollowers.append(u)
		for u in user2.followers.keys():
			if u not in userFollowers:
				userFollowers.append(u)

		cosineFollowersNum = 0
		cosineFollowersDen1 = 0
		cosineFollowersDen2 = 0

		for u in userFollowers:
			if u in user1.followers and u in user2.followers:
				cosineFollowersNum += 1
			if u in user1.followers:
				cosineFollowersDen1 += 1
			if u in user2.followers:
				cosineFollowersDen2 += 1

		cosineFollowers = cosineFollowersNum / math.sqrt(cosineFollowersDen1 * cosineFollowersDen2)

		return (cosineFollowing + cosineFollowers) / 2

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
	def zhangSimilarity(self,user1,user2):
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

	"""Returns the cosine similarity of the two users using this similarity parameter
	Parameters:
	user1 - first user
	user2 - second user
	"""
	def cosine(self,user1,user2):
		hashtagDim = []

		for h in user1.hashtags.keys():
			if h not in hashtagDim:
				hashtagDim.append(h)

		for h in user2.hashtags.keys():
			if h not in hashtagDim:
				hashtagDim.append(h)

		cosineNum = 0
		cosineDen1 = 0
		cosineDen2 = 0

		for h in hashtagDim:
			if h in user1.hashtags and h in user2.hashtags:
				cosineNum += user1.hashtags[h] * user2.hashtags[h]

			if h in user1.hashtags:
				cosineDen1 += user1.hashtags[h] ** 2

			if h in user2.hashtags:
				cosineDen2 += user2.hashtags[h] ** 2

		return cosineNum / math.sqrt(cosineDen1 * cosineDen2)

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
	"""This class represents the retweeting similarity parameter"""

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
	def zhangSimilarity(self,user1,user2):
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

	"""Returns the cosine similarity of the two users using this similarity parameter
	Parameters:
	user1 - first user
	user2 - second user
	"""
	def cosine(self,user1,user2):
		retweetDim = []

		for h in user1.retweets.keys():
			if h not in retweetDim:
				retweetDim.append(h)

		for h in user2.retweets.keys():
			if h not in retweetDim:
				retweetDim.append(h)

		cosineNum = 0
		cosineDen1 = 0
		cosineDen2 = 0

		for h in retweetDim:
			if h in user1.retweets and h in user2.retweets:
				cosineNum += user1.retweets[h] * user2.retweets[h]

			if h in user1.retweets:
				cosineDen1 += user1.retweets[h] ** 2

			if h in user2.retweets:
				cosineDen2 += user2.retweets[h] ** 2

		return cosineNum / math.sqrt(cosineDen1 * cosineDen2)

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

class Mentions(Parameter):
	"""This class represents the mentions similarity parameter"""

	def __init__(self):
		Parameter.__init__(self)

	def commonMentions(self, user1, user2):
		mentions = []
		for r in user1.mentions:
			if r in user2.mentions.keys():
				mentions.append(r)
		return mentions

	"""Computes for mentions similarity
	Parameter:
	user1 - first user
	user2 - second user
	"""
	def zhangSimilarity(self,user1,user2):
		a = len(self.commonMentions(user1, user2))
		b1 = 0
		if user2.id in user1.mentions:
			b1 = user1.mentions[user2.id]
		b2 = 0
		if user1.id in user2.mentions:
			b2 = user2.mentions[user1.id]
		b = b1+b2
		if len(user1.mentions)==0 or len(user2.mentions)==0:
			a = 0
			b = 0
		else:
			a /= math.sqrt(len(user1.mentions))*math.sqrt(len(user2.mentions))
			b /= len(user1.mentions)*len(user2.mentions)
		return a+b

	"""Returns the cosine similarity of the two users using this similarity parameter
	Parameters:
	user1 - first user
	user2 - second user
	"""
	def cosine(self,user1,user2):
		mentionsDim = []

		for h in user1.mentions.keys():
			if h not in mentionsDim:
				mentionsDim.append(h)

		for h in user2.mentions.keys():
			if h not in mentionsDim:
				mentionsDim.append(h)

		cosineNum = 0
		cosineDen1 = 0
		cosineDen2 = 0

		for h in mentionsDim:
			if h in user1.mentions and h in user2.mentions:
				cosineNum += user1.mentions[h] * user2.mentions[h]

			if h in user1.mentions:
				cosineDen1 += user1.mentions[h] ** 2

			if h in user2.mentions:
				cosineDen2 += user2.mentions[h] ** 2

		return cosineNum / math.sqrt(cosineDen1 * cosineDen2)

	def createOutgoingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and userList[u].id in user.mentions.keys():
				edges[u] = 1
		return edges

	def createIncomingEdges(self, user, userList):
		edges = {}
		for u in userList:
			if user != userList[u] and user.id in userList[u].mentions.keys():
				edges[u] = 1
		return edges