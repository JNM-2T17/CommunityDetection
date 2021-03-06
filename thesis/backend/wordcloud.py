import json
import operator

# Counts the number of words per community from a JSON file and writes to another JSON file
def countWords(readFile, writeFile):
	minSize = 10
	maxSize = 50

	print("wordcloud.py: Load JSON file");
	# Load JSON file containing tweets
	with open(readFile, encoding="utf8") as f:
		line = f.readline()
		data = json.loads(line)

	cWordCounts = {}
	cWordMinMax = {}

	print("wordcloud.py: Count instances of each word per community");
	# Count instances of each word per community
	for key, value in data.items():
		wordCounts = {}

		for l in value["string"]:
			l = l.replace('\n', ' ').split()
			for word in l:
				if word[0]!='@' and not word.startswith('http://') and not word.startswith('https://'):
					word = cleanWord(word)
					if word in wordCounts:
						wordCounts[word] += 1
					else:
						wordCounts[word] = 1

		cWordCounts[key] = wordCounts
		cWordMinMax[key] = {"maxCount" : 1, "minCount" : float("inf")}

	print("wordcloud.py: Remove common words");
	# Remove words that are too common
	if len(cWordCounts) > 1:
		for key, value in cWordCounts["1"].copy().items():
			inAllDict = True

			for key2, value2 in cWordCounts.items():
				if not key in value2.keys() and data[key2]["size"] > 2:
					inAllDict = False
					break
			if inAllDict:
				for c in cWordCounts:
					cWordCounts[c].pop(key, None)

	print("wordcloud.py: Adjust size values");
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

	print("wordcloud.py: Convert to JSON format");
	# Convert to JSON format
	finalCounts = {}

	for key, value in cWordCounts.items():
		finalCounts[key] = []

		for key2, value2 in sorted(value.items(), key=operator.itemgetter(1), reverse = True):
			finalCounts[key].append({"text": key2, "size": value2})

	print("wordcloud.py: Write to file");
	with open(writeFile, 'w') as outputFile:
		json.dump(finalCounts, outputFile)

# Removes unnecessary characters and case
def cleanWord(word):
	word = word.lower()
	word = word.replace('.', '').replace('!', '').replace('?', '').replace(',', '').replace('\'', '').replace('…', '').replace('"', '').replace('(', '').replace(')', '').replace('[', '').replace(']', '')
	return word

