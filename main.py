from TopSort import *
import time
timestart= time.perf_counter()
#import the edge list converter
#import the adjacencybuilder

#Take in the directed acyclic graph file into memory

#build edge list graph -> something like edgelist = graphBuilder(Research Rabbit)

#adjacencyList = adjacencyBuilder(edgelist) ->dfs to check for circular edges

#pass adjacency list into topoligical sort -> sortedList = Top.topologicalSort(adjacencyList)
adjacencyList = {}
sortedList = TopSort.topologicalSort(adjacencyList)

timestop = time.perf_counter()

print(sortedList)
print(f"Time to Execute {timestop-timestart}")
#I want to make it print out the links, but I don't want to skip too far ahead since the rest of the project isn't done
