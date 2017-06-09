import json

users = []
with open("Demo Tweet Data/user_dataset.json", encoding="utf8") as f:
	for line in f:
		data = json.loads(line)
		users.append(data)

with open("Demo Tweet Data/tweets.json", encoding="utf8") as f:
	for line in f:
		data = json.loads(line)
		uId = data["id"]
		if isinstance(uId, dict):
			uId = uId["$numberLong"]
		for u in users:
			if u["id"] == uId:
				u["tweets"] = data["tweets"]
				break

with open("Demo Tweet Data/following.json", encoding="utf8") as f:
	for line in f:
		data = json.loads(line)
		uId = data["id"]
		if isinstance(uId, dict):
			uId = uId["$numberLong"]
		for u in users:
			if u["id"] == uId:
				u["following_ids"] = data["following_ids"]
				break

print("Writing json...")
with open('Demo Tweet Data/compressed.json', 'w') as outfile:
    for u in users:
    	json.dump(u, outfile)
    	outfile.write("\n")
