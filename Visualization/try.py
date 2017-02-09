from igraph import *

g = Graph()
g.add_vertices(3)
g.add_edges([(0,1), (1,2)])
print(g)