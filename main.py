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
    edgeList = [("Paper D","Paper B"),("Paper D","Paper C"),("Paper B","Paper A"),("Paper B","Paper A")]

#adjacencyList = adjacencyBuilder(edgelist) ->dfs to check for circular edges

#Hardcoding adjacency list to test
adjacencyList={"Paper D": ["Paper B", "Paper C"],"Paper B": ["Paper A"],"Paper C": ["Paper A"]}
FileSetuptimestop= time.perf_counter()

adjtimestart = time.perf_counter()
#pass adjacency list into topoligical sort -> sortedList = Top.topologicalSort(adjacencyList)
sortedList = TopSort.topologicalSort(adjacencyList)
adjtimestop = time.perf_counter()
print(f"List Is Verified: {TopSort.verifySort(sortedList)}")

edgetimestart = time.perf_counter()
sortedListEdge = TopSort.topologicalEdgeSort(edgeList)
edgetimestop = time.perf_counter()
print(f"Sorted Adjacency List: {sortedList}")
print(f"Sorted Edge List: {sortedListEdge}")
print(f"Time to create Unsorted List:{FileSetuptimestop-FileSetuptimestart}")
print(f"Time to Sort Adjacency List: {adjtimestop-adjtimestart}")
print(f"Time to Sort Edge List: {edgetimestop-edgetimestart}")
#I want to make it print out the links, but I don't want to skip too far ahead since the rest of the project isn't done
