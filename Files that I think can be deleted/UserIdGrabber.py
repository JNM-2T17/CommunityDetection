from FolderIO import FolderIO
from JSONParser import JSONParser
import csv

dirname = "C:/Users/Marc Dominic/Documents/Thesis/Tweet Data"
folderIO = FolderIO()
files = folderIO.get_files(dirname, False, ".json") 
print("Found {} files.".format(len(files)))

jsonParser = JSONParser()
idList = []
existingIds = {}
for file in files:
	for tweet_json in jsonParser.parse_file_into_json_generator(file):
		user = tweet_json["user"]
		id = user["id"]
		if id not in existingIds:
			idList.append(id)
			existingIds[id] = True
print("Found", len(idList), "unique ids")

print("Writing to output file...")
with open(dirname+"/UsersList.csv", "w") as out:
    wr = csv.writer(out)
    wr.writerow(idList)
print("Finished writing successfully.")