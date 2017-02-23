from Model import *
import json

def load_user_friendships(dirname, userIdFilename, ffFilename):
	# dirname = "C:/Users/Marc Dominic/Documents/Thesis/Tweet Data"
	# userIdFilename = "/TestUsersList.csv"

	idList = []
	with open(dirname+userIdFilename, encoding="utf8") as f:
		for line in f:
			id = json.loads(line)["id"]
			if isinstance(id, dict):
				id = id["$numberLong"]
			idList.append(id)
	idList = set(idList)
	print("Loaded", len(idList), "unique ids")
	users = {}
	for id in idList:
		users[id] = User(id)
	print("Created", len(users), "users")

	# ffFilename = "/TestFFIds.csv"
	with open(dirname+ffFilename, encoding="utf8") as f:
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

	return users