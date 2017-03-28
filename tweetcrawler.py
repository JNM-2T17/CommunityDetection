import json
import tweepy

auth = tweepy.OAuthHandler("Oin4lfEnrOSxAdvadE77u1TmA", "WAzwlBWykKt18WG7Za6JadpJHgR2mkldN8mPgzsU2MFk6tzaQg")
auth.set_access_token("2355697038-vbX1vt6liw7PI4DAR4tEDy3BuZpIzmgpIDUsnvi", "WHM4qY76ZAMRDbWoFBDJxuOTkyRccpE4iiv9IkfbJ4cOl")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

dirname = "C:/Users/Marc/Documents/CommunityDetection/Demo Tweet Data/"
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
	try:
		print(ctr, " - Reading", srcId, "'s tweets")
		tweets = api.user_timeline(id=srcId, count=100, include_entities=True)
		entry["tweets"] = []
		for x in tweets:
			entry["tweets"].append(x._json)	
		data.append(entry)
	except Exception as e:
		print("{}".format(e))

with open(dirname+"tweets.json", 'w') as out:
	for entry in data:
		json.dump(entry, out)
		out.write("\n")