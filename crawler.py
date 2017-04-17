from FolderIO import FolderIO
from JSONParser import JSONParser
import json
import tweepy

auth = tweepy.OAuthHandler("Oin4lfEnrOSxAdvadE77u1TmA", "WAzwlBWykKt18WG7Za6JadpJHgR2mkldN8mPgzsU2MFk6tzaQg")
auth.set_access_token("2355697038-vbX1vt6liw7PI4DAR4tEDy3BuZpIzmgpIDUsnvi", "WHM4qY76ZAMRDbWoFBDJxuOTkyRccpE4iiv9IkfbJ4cOl")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# with open('dlsu_users.json', 'w') as outfile:
# 	for i in range(1, 11):
# 		keyword = "DLSU"
# 		users = api.search_users(keyword, page=i)
# 		print(len(users))
# 		print("Writing json...")
# 		for u in users:
# 			if keyword not in u.name and keyword not in u.screen_name: 
# 				json.dump(u._json, outfile)
# 				outfile.write("\n")

# with open('admu_users.json', 'w') as outfile:
# 	for i in range(1, 11):
# 		keyword = "ADMU"
# 		users = api.search_users(keyword, page=i)
# 		print(len(users))
# 		print("Writing json...")
# 		for u in users:
# 			if keyword not in u.name and keyword not in u.screen_name: 
# 				json.dump(u._json, outfile)
# 				outfile.write("\n")

with open('up_users.json', 'w') as outfile:
	for i in range(1, 11):
		keyword = "Diliman"
		users = api.search_users(keyword, page=i)
		print(len(users))
		print("Writing json...")
		for u in users:
			if keyword not in u.name and keyword not in u.screen_name: 
				json.dump(u._json, outfile)
				outfile.write("\n")

# with open('ust_users.json', 'w') as outfile:
# 	for i in range(1, 11):
# 		keyword = "UST"
# 		users = api.search_users(keyword, page=i)
# 		print(len(users))
# 		print("Writing json...")
# 		for u in users:
# 			if keyword not in u.name and keyword not in u.screen_name: 
# 				json.dump(u._json, outfile)
# 				outfile.write("\n")


# ffList = []
# ctr = 0
# for srcId in idList:
# 	for tgtId in idList:
# 		if srcId != tgtId:
# 			ctr+=1
# 			print(ctr, "- Checking relationship between", srcId, "and", tgtId)
# 			rel = api.show_friendship(source_id=srcId, target_id=tgtId)
# 			src, tgt = rel
# 			if src.following:
# 				ffList.append([srcId, tgtId])
# with open(dirname+"/TestFFIds.csv", 'w') as out:
# 	wr = csv.writer(out);
# 	for r in ffList:
# 		wr.writerow(r)
# print(len(ffList))
