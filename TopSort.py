from collections import deque
from io import *
import csv
class TopSort:
    #Referencing Kahn's BFS Topological Sorting Algorithm, Just the concept, not the code
    #We decided on using adjacency lists from researching Kahn's algo -> dictionaries are easier to iterate through compared to 2d lists

    #I'm writing this code before my partners and I just want to ensure only the adjacency list gets passed through
    def topologicalSort(inputList: dict) -> list:
        sortedList = []
        #How many nodes are pointing at a specific node is called in-degree
        inDegree = {}
        #Kahn's algo uses BFS, which I learned by using queues
        bfsQueue = deque()

        #Reminder to self -> Don't forget to explain why top sort needs in-degrees first
        #Iterate through Nodes and add their associated in-degrees.
        for Node in inputList:
            inDegree.setdefault(Node,0)
            for connectedNodes in inputList[Node]:
                inDegree.setdefault(connectedNodes,0)
                inDegree[connectedNodes] +=1
        
        for Node in inDegree:
            #If the in-degree is 0, this can be added first as nothing points to it
            #BFS needs parent nodes to start with
            if (inDegree[Node]==0):
                bfsQueue.append(Node)
        

        while (len(bfsQueue)!=0):
            #So it'll pop the first node, add it's children to the queue.
            firstNode = bfsQueue.popleft()
            sortedList.append(firstNode)
            #Edge case where the list somehow has the node as a dependency, but not as a key
            for connectedNodes in inputList.get(firstNode,[]):
                #We just popped the connected node, so it has 1 less incoming edge ie reduce indegrees by 1.
                inDegree[connectedNodes] -=1
                #This paper no longer has any incoming edges left->The paper that was citing this has already been added
                if inDegree[connectedNodes]==0:
                    bfsQueue.append(connectedNodes)
                else:
                    continue
            

        #My logic was that the papers that were cited the most should be foundational knowledge for papers that have no or few citations
        #From Kahn's algo, the papers that are not cited by anything ie indegree =0 come first.
        #return sortedList[::-1] -> Originally it was like this, but Pushpdeep implemented a way to get a reversed edge list where old paper->new paper                
        return sortedList
    
    #I got the idea to compare the performance of an adjacency list against the edgelist
    #Keeping everything static apart from the in-degree setup
    def topologicalEdgeSort(inputlist:list)->list:
        sortedList = []
        inDegree = {}
        bfsQueue = deque()

        #Should take longer since the connectedNodes aren't all placed in one key
        for pairs in inputlist:
            Node = pairs[0]
            inDegree.setdefault(Node,0)
            if pairs[1]:
                connectedNode = pairs[1]
                inDegree.setdefault(connectedNode,0)
                inDegree[connectedNode]+=1

        for nodes in inDegree:
            if inDegree[nodes]==0:
                bfsQueue.append(nodes)
        
        
        while (len(bfsQueue)!=0):
            firstNode = bfsQueue.popleft()
            sortedList.append(firstNode)
            #I had to change this step, I can't just look for the key from the pairs
            for pair in inputlist:
                if pair[0]==firstNode:
                    connectedNode = pair[1]
                    inDegree[connectedNode] -=1
                    if inDegree[connectedNode]==0: 
                        bfsQueue.append(connectedNode)
        #Originally it was sortedList[::-1], but Pushpdeep implemented a way to get a reversed edge list where old paper->new paper                
        return sortedList
    
    #This verifysort function is no longer viable, there are too many viable sorted list orders 
    #def verifySort(list)->bool:
    
    #Extract Data and write.
    #Sorted Edge List should be identical or a viable variation of the sorted Adjacency list
    def finalFile(sortedAdjacencyList,csvFile):
        Papers =[]
        with open(csvFile, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))  # Load once
            for RRabbitID in sortedAdjacencyList:
                for rows in reader:
                    if ((rows["ResearchRabbitId"]).strip())==RRabbitID:
                        #Credit goes to Jang for extracting information from csv ->Code segment from commit that had to be reverted due to it replacing a partner's code
                        doi = (rows["DOI"])
                        year = (rows["Year"])
                        title = (rows["Title"])
                        link = "(no link)"
                        if doi and doi != "(missing DOI)":
                            link = f"https://doi.org/{doi}"   
                        Papers.append(f"{doi},{year},{title},{link}")
                        break
        
        with open("Sorted Papers.csv","w",encoding="utf-8") as file:
            file.write("DOI,Year,Title,Link\n")
            for paper in Papers:
                file.write(f"{paper}\n")
            