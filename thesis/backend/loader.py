from .model import *
import json

class Loader:

	def __init__(self, filename):
		self.filename = filename

	def load_user_friendships(self):
		idList = []
		userInfo = {}
		userList = []
		with open(self.filename, encoding="utf8") as f:
			for line in f:
				cur = json.loads(line)
				userList.append(cur)
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

		readIds = []
		for data in userList:
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
			if data["id"] not in readIds:
				readIds.append(data["id"])
				user = users[data["id"]]
				if "tweets" in data.keys():
					for t in data["tweets"]:
						tweetdata = t
						user.tweets.append(Tweet(tweetdata))
						if "hashtags" in tweetdata["entities"].keys():
							for h in tweetdata["entities"]["hashtags"]:
								hText = h["text"].lower()
								if hText in user.hashtags.keys():
									user.hashtags[hText] += 1
								else:
									user.hashtags[hText] = 1
						if "retweeted_status" in tweetdata.keys():
							retweetedId = tweetdata["retweeted_status"]["user"]["id"]
							if retweetedId in user.retweets.keys():
								user.retweets[retweetedId] += 1
							else:
								user.retweets[retweetedId] = 1
		return users