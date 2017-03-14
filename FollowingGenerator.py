import json
import tweepy

auth = tweepy.OAuthHandler("Oin4lfEnrOSxAdvadE77u1TmA", "WAzwlBWykKt18WG7Za6JadpJHgR2mkldN8mPgzsU2MFk6tzaQg")
auth.set_access_token("2355697038-vbX1vt6liw7PI4DAR4tEDy3BuZpIzmgpIDUsnvi", "WHM4qY76ZAMRDbWoFBDJxuOTkyRccpE4iiv9IkfbJ4cOl")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

dirname = "C:/Users/Marc/Documents/CommunityDetection/Tweet Data/"
userIdFilename = "user_dataset.json"

idList = []
with open(dirname+userIdFilename, encoding="utf8") as f:	
	for line in f:
		data = json.loads(line)
		id = data["id"]
		if isinstance(id, dict):
			id = id["$numberLong"]
		idList.append(id)
print("Imported", len(idList), "ids")

data = []
ctr = 0
for srcId in idList:
	ctr+=1
	entry = {}
	entry["id"] = srcId
	entry["following_ids"] = []
	try:
		print(ctr, " - Reading", srcId, "'s friends")
		friends = api.friends_ids(id=srcId)
		for tgtId in idList:
			if tgtId in friends:
				entry["following_ids"].append(tgtId)
	except Exception as e:
		print("{}".format(e))
	data.append(entry)

with open(dirname+"following.json", 'w') as out:
	for entry in data:
		json.dump(entry, out)
		out.write("\n")