from model import *
import json

class Loader:

	def __init__(self, dirname, userIdFilename, ffFilename):
		self.dirname = dirname
		self.userIdFilename = userIdFilename
		self.ffFilename = ffFilename
		self.m = 0

	def load_user_friendships(self):

		idList = []
		userInfo = {}
		with open(self.dirname+self.userIdFilename, encoding="utf8") as f:
			for line in f:
				cur = json.loads(line)
				id = cur["id"]
				if isinstance(id, dict):
					id = id["$numberLong"]
				idList.append(id)
				userInfo[id] = cur
		idList = set(idList)
		print("Loaded", len(idList), "unique ids")
		users = {}
		for id in idList:
			users[id] = User(id)
			users[id].saveJson(userInfo[id])
		print("Created", len(users), "users")

		with open(self.dirname+self.ffFilename, encoding="utf8") as f:
			for line in f:
				data = json.loads(line)
				id = data["id"]
				if isinstance(id, dict):
					id = id["$numberLong"]
				if id in users:
					followingIds = data["following_ids"]
					for tgtId in followingIds:
						if isinstance(tgtId, dict):
							tgtId = tgtId["$numberLong"]
						if tgtId in users:
							users[id].follow(users[tgtId])
							self.m+=1
		toDelete = []
		for i in users:
			if users[i].countNetworkSize() == 0:
				toDelete.append(i)
		for i in toDelete:
			del users[i]
		return users