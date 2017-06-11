import json
import operator

# Counts the number of words per community from a JSON file and writes to another JSON file
def countWords(readFile, writeFile):
	minSize = 15
	maxSize = 70

	# Load JSON file containing tweets
	with open(readFile, encoding="utf8") as f:
		line = f.readline()
		data = json.loads(line)

	cWordCounts = {}
	cWordMinMax = {}

	# Count instances of each word per community
	for key, value in data.items():
		wordCounts = {}

		words = []

		for l in value:
			words = words + l.replace('\n', ' ').split()

		for w in words:
			word = cleanWord(w)

			if word in wordCounts:
				wordCounts[word] = wordCounts[word] + 1
			else:
				wordCounts[word] = 1

		cWordCounts[key] = wordCounts
		cWordMinMax[key] = {"maxCount" : 1, "minCount" : float("inf")}

	# Remove words that are too common
	if len(cWordCounts) > 1:
		for key, value in cWordCounts["1"].copy().items():
			inAllDict = True

			for key2, value2 in cWordCounts.items():
				if not key in value2.keys():
					inAllDict = False
					break

			if inAllDict:
				for c in cWordCounts:
					cWordCounts[c].pop(key, None)

	# Remove mentions
	for key, value in cWordCounts.items():
		for key2, value2 in value.copy().items():
			if key2[:1] == "@" or key2.startswith("http://") or key2.startswith("https://"):
				cWordCounts[key].pop(key2, None)

	# Adjust size values
	for key, value in data.items():
		for key2, value2 in cWordCounts[key].items():
			if value2 < cWordMinMax[key]["minCount"]:
				cWordMinMax[key]["minCount"] = value2
			if value2 > cWordMinMax[key]["maxCount"]:
				cWordMinMax[key]["maxCount"] = value2

		for key2, value2 in cWordCounts[key].items():
			if cWordMinMax[key]["maxCount"] == cWordMinMax[key]["minCount"]:
				cWordCounts[key][key2] = minSize
			else:
				cWordCounts[key][key2] = (value2 - 1) / (cWordMinMax[key]["maxCount"] - 1) * maxSize + minSize

	# Convert to JSON format
	finalCounts = {}

	for key, value in cWordCounts.items():
		finalCounts[key] = []

		for key2, value2 in sorted(value.items(), key=operator.itemgetter(1), reverse = True):
			finalCounts[key].append({"text": key2, "size": value2})

	with open(writeFile, 'w') as outputFile:
		json.dump(finalCounts, outputFile)

# Removes unnecessary characters and case
def cleanWord(word):
	word = word.lower()
	word = word.replace('.', '').replace('!', '').replace('?', '').replace(',', '').replace('\'', '').replace('…', '').replace('"', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')
	return word

# countWords("communitytweets.json", "wordCounts.json")