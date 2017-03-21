def countWords(readFile, writeFile):
	minSize = 15
	maxSize = 75

	with open(readFile, 'r') as inputFile:
		words = inputFile.read().replace('\n', ' ').split()

	wordCounts = {}
	maxCount = 1
	minCount = float("inf")

	for w in words:
		word = w.lower()

		if isSignificantWord(word):
			if word in wordCounts:
				wordCounts[word] = wordCounts[word] + 1

				if wordCounts[word] > maxCount:
					maxCount = wordCounts[word]
			else:
				wordCounts[word] = 1

	for key, value in wordCounts.items():
		if value < minCount:
			minCount = value

	for key, value in wordCounts.items():
		if maxCount == minCount:
			wordCounts[key] = minSize
		else:
			wordCounts[key] = (value - 1) / (maxCount - 1) * maxSize + minSize

	with open(writeFile, 'w') as outputFile:
		outputFile.truncate()
		outputFile.write("{\n\t\"wordCloud\": [\n")

		arraySize = len(wordCounts.items())
		arrayCurr = 0

		for key, value in wordCounts.items():
			arrayCurr += 1
			
			outputFile.write("\t\t{\n\t\t\t\"text\" : \"" + key + "\", \n\t\t\t\"size\" : " + str(value) + "\n\t\t")

			if not arrayCurr is arraySize:
				outputFile.write("},\n")

			else:
				outputFile.write("}\n")

		outputFile.write("\t]\n}")
		outputFile.close()

def isSignificantWord(word):
	exceptions = ["the", "and", "a", "is", "are", "in", "to", "that", "of"]

	if word in exceptions:
		return False

	else:
		return True


countWords("words.txt", "wordCounts.json")