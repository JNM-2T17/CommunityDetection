from model import *
import csv

def load_user_friendships(dirname, userIdFilename, ffFilename):
	# dirname = "C:/Users/Marc Dominic/Documents/Thesis/Tweet Data"
	# userIdFilename = "/TestUsersList.csv"

	idList = []
	with open(dirname+userIdFilename, 'r') as f:
		r = csv.reader(f)
		for row in r:
			for id in row:
				idList.append(id)
	print("Loaded", len(idList), "unique ids")

	users = {}
	for id in idList:
		users[id] = User(id)
	print("Created", len(users), "users")

	# ffFilename = "/TestFFIds.csv"
	with open(dirname+ffFilename, 'r') as f:
		r = csv.reader(f)
		for row in r:
			if len(row)>=1:
				srcId = row[0]
				tgtId = row[1]
				users[srcId].follow(users[tgtId])

	return users