import json
import sys

def clean(tweet):
	cleaned_tweet = {}
	cleaned_tweet["id"] = tweet["id"]
	cleaned_tweet["id_str"] = tweet["id_str"]
	cleaned_tweet["text"] = tweet["text"]
	cleaned_tweet["entities"] = tweet["entities"]
	if "retweeted_status" in tweet.keys():
		cleaned_tweet["retweeted_status"] = tweet["retweeted_status"]
	return cleaned_tweet

users = []
dirname = "Tiny Tweet Data/"
with open(dirname+"user_dataset.json", encoding="utf8") as f:
	for line in f:
		data = json.loads(line)
		data["following_ids"] = []
		users.append(data)
print("Loaded", len(users), "users")

with open(dirname+"following.json", encoding="utf8") as f:
	for line in f:
		data = json.loads(line)
		uId = data["id"]
		if isinstance(uId, dict):
			uId = uId["$numberLong"]
		for u in users:
			if u["id"] == uId:
				u["following_ids"] = data["following_ids"]
				break
print("Finished loading following network")

with open(dirname+"compressed.json", "w") as outfile:
	ctr = 1
	with open(dirname+"tweets.json", encoding="utf8") as f:
		for line in f:
			print("Reading line", ctr)
			ctr+=1
			data = json.loads(line)
			uId = data["id"]
			if isinstance(uId, dict):
				uId = uId["$numberLong"]
			raw_tweets = data["tweets"]
			filtered_tweets = []
			for t in raw_tweets:
				filtered_tweets.append(clean(t))
			for u in users:
				if u["id"] == uId:
					u["tweets"] = filtered_tweets
					json.dump(u, outfile)
					outfile.write("\n")
					del u
					break

print("Finished writing json")