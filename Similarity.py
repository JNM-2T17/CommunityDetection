from Model import *
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
		print(users)

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

		print(averageUser.id, averageUser.following, averageUser.followers)

		return averageUser