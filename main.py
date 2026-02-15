from TopSort import *
import time
import csv
from Graph_conversion import *
from TopSort import *
#import the edge list converter
#import the adjacencybuilder

CSVFILE = ""
FileSetuptimestart= time.perf_counter()
try:
    edgeList = load_citation_data(CSVFILE)
except:
    print("testing-We don't have a csv yet")

#adjacencyList = adjacencyBuilder(edgelist) ->dfs to check for circular edges

#Hardcoding adjacency list to test
adjacencyList={"Paper D": ["Paper B", "Paper C"],"Paper B": ["Paper A"],"Paper C": ["Paper A"]}
FileSetuptimestop= time.perf_counter()

timestart = time.perf_counter()
#pass adjacency list into topoligical sort -> sortedList = Top.topologicalSort(adjacencyList)
sortedList = TopSort.topologicalSort(adjacencyList)
print(f"List Is Verified: {TopSort.verifySort(sortedList)}")
timestop = time.perf_counter()

print(sortedList)
print(f"Time to create Unsorted List:{FileSetuptimestop-FileSetuptimestart}")
print(f"Time to Sort {timestop-timestart}")
#I want to make it print out the links, but I don't want to skip too far ahead since the rest of the project isn't done
