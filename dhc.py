from model import *
from Similarity import *
from collections import *

class divisive_hc(Algorithm):

	def run(self, users):
		com = Community()
		userids = list(users.keys())
		for id in userids:
			com.addUser(users[id])

		current = [com]
		frontier = deque()
		frontier.append(com)
		prevmod = self.parameter.modularity(current)

		iterCount = 0
		# while there are communities to split
		while not frontier:
			print("Iteration", iterCount)
			iterCount+=1
			# get first community and split
			temp = frontier.popleft()
			kmeans = KMeans(self.parameter, 2)

			results = kmeans.run()
			t1 = results[0]
			t2 = results[1]

			# replace previous community with halves
			current.delete(temp)
			current.append(t1)
			current.append(t2)

			# get modularity
			mod = self.parameter.modularity(current)

			# if splitting worsened modularity
			if mod < prevmod:
				# remove new divisions and restore old whole
				current.pop()
				current.pop()
				current.append(temp)
			else:	 # if splitting improved modularity
				
				# if halves have more than one element, add to frontier
				if len(t1) > 0:
					frontier.append(t1)
				
				if len(t2) > 0:
					frontier.append(t2)

				# update modularity
				prevmod = mod

		return current
