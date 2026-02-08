from collections import deque

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
            #If the in-degree is 0, this can be read first as nothing points to it
            if (inDegree[Node]==0):
                bfsQueue.append(Node)
        

        

        

        