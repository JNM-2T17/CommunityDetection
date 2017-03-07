from FolderIO import FolderIO
from JSONParser import JSONParser
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
# rel = api.show_friendship(source_id=2355697038, target_id=1222576416)
# src, tgt = rel
# print(src.following)

data = []
ctr = 0
start = 0
end = 25
for srcId in idList:
	entry = {}
	entry["id"] = srcId
	entry["following_ids"] = []
	for tgtId in idList:
		if srcId != tgtId:
			try:
				ctr+=1
				print(ctr, "- Checking relationship between", srcId, "and", tgtId)
				rel = api.show_friendship(source_id=srcId, target_id=tgtId)
				src, tgt = rel
				if src.following:
					entry["following_ids"].append(tgtId)
			except Exception as e:
				print("{}".format(e))
	data.append(entry)

with open(dirname+"following.json", 'w') as out:
	for entry in data:
		json.dump(entry, out)
		out.write("\n")