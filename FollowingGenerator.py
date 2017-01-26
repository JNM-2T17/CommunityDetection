from FolderIO import FolderIO
from JSONParser import JSONParser
import csv
import tweepy

auth = tweepy.OAuthHandler("Oin4lfEnrOSxAdvadE77u1TmA", "WAzwlBWykKt18WG7Za6JadpJHgR2mkldN8mPgzsU2MFk6tzaQg")
auth.set_access_token("2355697038-vbX1vt6liw7PI4DAR4tEDy3BuZpIzmgpIDUsnvi", "WHM4qY76ZAMRDbWoFBDJxuOTkyRccpE4iiv9IkfbJ4cOl")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

dirname = "C:/Users/Marc Dominic/Documents/Thesis/Tweet Data"
userIdFilename = "/TestUsersList.csv"
idList = []
with open(dirname+userIdFilename, 'r') as f:
	r = csv.reader(f)
	for row in r:
		for id in row:
			idList.append(id)

print("Imported", len(idList), "ids")
# rel = api.show_friendship(source_id=2355697038, target_id=1222576416)
# src, tgt = rel
# print(src.following)

ffList = []
ctr = 0
for srcId in idList:
	for tgtId in idList:
		if srcId != tgtId:
			ctr+=1
			print(ctr, "- Checking relationship between", srcId, "and", tgtId)
			rel = api.show_friendship(source_id=srcId, target_id=tgtId)
			src, tgt = rel
			if src.following:
				ffList.append([srcId, tgtId])
with open(dirname+"/TestFFIds.csv", 'w') as out:
	wr = csv.writer(out);
	for r in ffList:
		wr.writerow(r)
print(len(ffList))
