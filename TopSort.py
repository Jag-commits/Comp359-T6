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
            #If the in-degree is 0, this can be added first as nothing points to it
            #BFS needs parent nodes to start with
            if (inDegree[Node]==0):
                bfsQueue.append(Node)
        

        while (bfsQueue):
            #So it'll pop the first node, add it's children to the queue.
            firstNode = bfsQueue.popleft()
            #Edge case where the list somehow has the node as a dependency, but not as a key
            for connectedNodes in inputList.get(firstNode,[]):
                #We just popped the connected node, so it has 1 less incoming edge ie reduce indegrees by 1.
                inDegree[connectedNodes] -=1
                #This paper no longer has any incoming edges left->The paper that was citing this has already been added
                if inDegree[connectedNodes]==0:
                    bfsQueue.append(connectedNodes)
                else:
                    continue
            sortedList.append(firstNode)

        #My logic was that the papers that were cited the most should be foundational knowledge for papers that have no or few citations
        #From Kahn's algo, the papers that are not cited by anything ie indegree =0 come first.
        return sortedList[::-1]

    inputList = {"D": ["B", "C"],"B": ["A"],"C": ["A"],"A": []}
    #The list doesn't have A as key test case
    inputList2 = {"D": ["B", "C"],"B": ["A"],"C": ["A"]}
    print(topologicalSort(inputList))
    print(topologicalSort(inputList2))

        

        

        