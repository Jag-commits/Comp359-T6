from TopSort import *
import time
from Graph_conversion import *
from TopSort import *
from adjacency_builder import *
global edgeList,adjacencyList
edgelist = []
adjacencyList = {}

CSVFILE = "articles.csv"
FileSetuptimestart= time.perf_counter()
try:
    pairs = load_citation_data(CSVFILE)
    #No clue what part made adjacency list sort slower, maybe it's the long strings
    edgeList = build_edges(pairs,True,False)
    edgeList= edgeList[0]
except:
    #Failsafe, if the edgelist couldn't be made
    edgeList = [("Paper D","Paper B"),("Paper D","Paper C"),("Paper B","Paper A"),("Paper B","Paper A")]

try:
    #Note: I had to revert commit history (And recommit specific files on the behalf of the partner) because of a miscommunication.
    adjacencyList = adjacency_builder.adjacencyBuilder(edgeList,None)
    DAGTrue= adjacency_builder.is_dag(adjacencyList)
    if (DAGTrue!=True):
        print("Graph is not DAG")
        raise Exception("Graph is not DAG")
    
except:
    #Failsafe if edgelist conversion failed
    adjacencyList={"Paper D": ["Paper B", "Paper C"],"Paper B": ["Paper A"],"Paper C": ["Paper A"]}


FileSetuptimestop= time.perf_counter()

adjtimestart = time.perf_counter()
#pass adjacency list into topoligical sort -> sortedList = Top.topologicalSort(adjacencyList)
sortedList = TopSort.topologicalSort(adjacencyList)
adjtimestop = time.perf_counter()

edgetimestart = time.perf_counter()
sortedListEdge = TopSort.topologicalEdgeSort(edgeList)
edgetimestop = time.perf_counter()

print(f"Sorted Adjacency List: {sortedList}")
print(f"Sorted Edge List: {sortedListEdge}")
print(f"Time to create Unsorted List:{FileSetuptimestop-FileSetuptimestart}")
print(f"Time to Sort Adjacency List: {adjtimestop-adjtimestart}")
print(f"Time to Sort Edge List: {edgetimestop-edgetimestart}")
#Create a file to store the ordered list of papers permantently
TopSort.finalFile(sortedList,"articles.csv")
print("File of Sorted Papers Created Successfully")
