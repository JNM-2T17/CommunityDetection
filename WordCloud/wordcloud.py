import json
import operator

def countWords(readFile, writeFile):
	minSize = 15
	maxSize = 75

	with open(readFile, encoding="utf8") as f:
		line = f.readline()
		data = json.loads(line)

	cWordCounts = {}

	for key, value in data.items():
		wordCounts = {}
		maxCount = 1
		minCount = float("inf")

		words = []

		for l in value:
			words = words + l.replace('\n', ' ').split()

		for w in words:
			word = cleanWord(w)

			if isSignificantWord(word):
				if word in wordCounts:
					wordCounts[word] = wordCounts[word] + 1

					if wordCounts[word] > maxCount:
						maxCount = wordCounts[word]
				else:
					wordCounts[word] = 1

		for key2, value2 in wordCounts.items():
			if value2 < minCount:
				minCount = value2

		for key2, value2 in wordCounts.items():
			if maxCount == minCount:
				wordCounts[key2] = minSize
			else:
				wordCounts[key2] = (value2 - 1) / (maxCount - 1) * maxSize + minSize
		cWordCounts[key] = wordCounts

	finalCounts = {}

	for key, value in cWordCounts.items():
		finalCounts[key] = []

		for key2, value2 in sorted(value.items(), key=operator.itemgetter(1), reverse = True):
			finalCounts[key].append({"text": key2, "size": value2})

	with open(writeFile, 'w') as outputFile:
		json.dump(finalCounts, outputFile)

def isSignificantWord(word):
	exceptions = ["the", "and", "a", "is", "are", "in", "to", "that", "of"]

	if word in exceptions:
		return False

	else:
		return True

def cleanWord(word):
	word = word.lower()
	word = word.replace('.', '').replace('!', '').replace('?', '').replace(',', '').replace('\'', '').replace('…', '').replace('"', '')
	return word

countWords("communityTweets.json", "wordCounts.json")