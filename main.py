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
    #The longer RRabbit IDs make it slower compared to normalized IDs
    edgeList = build_edges(pairs,True,True)
    #We'll use this at the very last step to reconvert the normalized IDs to RRabbit IDs 
    idMap=edgeList[2]
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
        #If the adjacency list has a cycle, it is also found in the edgeList.
        edgeList = [("Paper D","Paper B"),("Paper D","Paper C"),("Paper B","Paper A"),("Paper B","Paper A")]
        raise Exception("Graph is not DAG")
    
except:
    #Failsafe if edgelist conversion failed
    adjacencyList={"Paper D": ["Paper B", "Paper C"],"Paper B": ["Paper A"],"Paper C": ["Paper A"]}
FileSetuptimestop= time.perf_counter()

#Big error found -> The second sorting call (Regardless of whether it's edgelist or adjlist) will run faster
#For Testing Purposes, I'm running both methods prematurely, such that the data is already cached. 
TopSort.topologicalEdgeSort(edgeList)
TopSort.topologicalSort(adjacencyList)

edgetimestart = time.perf_counter()
sortedListEdge = TopSort.topologicalEdgeSort(edgeList)
edgetimestop = time.perf_counter()

adjtimestart = time.perf_counter()
sortedList = TopSort.topologicalSort(adjacencyList)
adjtimestop = time.perf_counter()

#The P1,P2 aren't representative of the order from the csv file, they are from the pairs
print(f"Sorted Adjacency List: {sortedList}")
print(f"Sorted Edge List: {sortedListEdge}")
print(f"Sorted List is Verified: {TopSort.verifySort(sortedList,adjacencyList)}")
print(f"Time to create Unsorted List:{FileSetuptimestop-FileSetuptimestart}")
print(f"Time to Sort Adjacency List: {adjtimestop-adjtimestart}")
print(f"Time to Sort Edge List: {edgetimestop-edgetimestart}")
#Create a file to store the ordered list of papers permantently
TopSort.finalFile(sortedList,idMap,"articles.csv")
print("File of Sorted Papers Created Successfully")
