from Model import *

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

		return (cFriend / (sqrt(len(user1.following) * len(user2.following))) + 
		 		cFollowers / (sqrt(len(user1.followers) * 
		 							len(user2.followers)))) 

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
				if userId in followerCount:
					followersCount[userId] += 1
				else:
					followersCount[userId] = 1

		numUsers = len(users)

		averageFollowing = {}

		for userId, count in followingCount:
			if count*1.0/numUsers >= numUsers/2:
				averageFollowing[userId] = users[userId]

		averageFollowers = {}

		for userId, count in followersCount:
			if count*1.0/numUsers >= numUsers/2:
				averageFollowers[userId] = users[userId]

		averageUser = User("Average")
		averageUser.following = averageFollowing
		averageUser.followers = averageFollowers

		return averageUser