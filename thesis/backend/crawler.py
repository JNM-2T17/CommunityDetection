import json
import tweepy

auth = tweepy.OAuthHandler("Oin4lfEnrOSxAdvadE77u1TmA", "WAzwlBWykKt18WG7Za6JadpJHgR2mkldN8mPgzsU2MFk6tzaQg")
auth.set_access_token("2355697038-vbX1vt6liw7PI4DAR4tEDy3BuZpIzmgpIDUsnvi", "WHM4qY76ZAMRDbWoFBDJxuOTkyRccpE4iiv9IkfbJ4cOl")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

final_ids = []
company_list = ["Atlus", "Sony", "Microsoft", "Nintendo", "Ubisoft", "Bethesda", "Naughty Dog", "Square Enix", "EA", "Kojima"]
coeff = 1

ctr = 1
for company in company_list: 
	print("Crawling tweets for", company)
	query = company+" E3 -filter:retweets -@Youtube"
	tweet_ids = []
	results = api.search(q=query, count=100, lang="en")
	for r in results:
		print(ctr, r.text)
		ctr+=1
		r = r._json
		tweet_ids.append(r["id"])
		if r["user"]["id"] not in final_ids:
			final_ids.append(r["user"]["id"])

	while len(final_ids) < coeff*250:
		results = api.search(q=query, count=100, max_id=min(tweet_ids), lang="en")
		for r in results:
			print(ctr, r.text)
			ctr+=1
			r = r._json
			tweet_ids.append(r["id"])
			if r["user"]["id"] not in final_ids:
				final_ids.append(r["user"]["id"])
			if len(final_ids)==coeff*250:
				break
	coeff+=1

with open('E3 Tweet Data/e3_users.json', 'w') as outfile:
	ctr = 1
	for currId in final_ids:
		print("Getting user", ctr)
		ctr+=1
		u = api.get_user(currId)
		json.dump(u._json, outfile)
		outfile.write("\n")
