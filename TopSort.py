from collections import deque

class TopSort:
    #Referencing Kahn's BFS Topological Sorting Algorithm, Just the concept, not the code
    #We decided on using adjacency lists from researching Kahn's algo -> dictionaries are easier to iterate through compared to 2d lists

    #I'm writing this code before my partners and I want to ensure only the adjacency list gets passed through
    def topologicalSort(inputList: dict) -> list:
        numOfNodes = len(inputList)
        #How many nodes are pointing at a specific node is called in-degree
        inDegree = {}
        #Kahn's algo uses BFS, which I learned by using queues
        queue = deque()
        
        #Set all the indegrees up -> I need a more efficient way
        for Node in inputList:
            inDegree[Node]=0

        for Node in inputList:
            for connectedNodes in inputList[Node]:
                inDegree[Node] +=1
        
        for Node in inputList:
            if (inDegree[Node]==0):
                queue.append