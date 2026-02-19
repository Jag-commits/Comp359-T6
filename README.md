COMP 359, ON 1 Assignment 2 README 

Responsibility Split: https://docs.google.com/document/d/1CNVFqzEXJpOW_nXpOcXWMrRaES8_cz77Pl4NT2S9Sik/edit?usp=sharing 

**Analysis Framework**

Independent Variables
- Unordered citation export (CSV)

Dependent Variables
- Ordered List of Papers (Foundational Knowledge->Newer Papers)
- Time to Convert CSV into adjacency list (HDD vs SSD)
- Time to sort adjacency list
- Time to sort edge list

Baseline for Verification:
- Initially, smaller lists enabled a verification process against manually checked variations in sorting order.
  But, as amount of papers increase, this process becomes impractical due to numerous variations.
  
Evaluation Method
- The citation graph csv is loaded into memory
- The citation csv is first converted into an edgelist.
- Each edge is mapped into an adjacency list and checked for cycles
- The time to sort an edge list and the associated adjacency list are compared
  
Failure Conditions
- Missing Nodes/Papers in the topological sorting output.
- Newer Papers appear before the papers they cite in final list
- Citation Graph has cycles

Constraints
- Nodes are limited to <=8 Papers.

Design Decisions
- The algorithm uses adjacency lists as opposed to a 2d matrix. This is because 2d arrays require the program to iterate through each of the sub arrays to determine which nodes are connected to other nodes, leading to O(n^2) time complexity. Adjacency lists, as dictionaries can store the connected nodes, meaning the program just needs to iterate through the key value pairs leading to O(n+m) time complexiy.
- The topological sort ordering is based on the most number of in-degrees(Incoming edges/incoming citations) to least number of in-degrees. This is ordering is the reverse of the traditional topological sorting output. The algorithm reverses the ordering, since the newer papers build off of the knowledge from previous papers.
- The program intially created adjacency lists with the format Citing Paper -> Referenced Paper, however, changes in the edge list creation class enables for reversing this edge list as Referenced Paper ->Citing Paper. This change enables the topological sort to output a list in the order Foundational Paper ->Newer Papers. This means the program is actually using out-degrees rather than in-degrees.
- For measuring the speed of sorting the adjacency list compared to the edge list, the second sort call would be consistently faster than the first. It did not matter whether this was the adjacency list or edge list (The adjacency list should have been faster). This could have been caused by node values being cached during the first sorting call, and reused during the second call. To keep the measurements accurate, both sorting algorithms were called prior to measurements, this fixed our skewed results issue. This change is only for measurement purposes, otherwise the program should only use adjacency lists for maximum sorting performance.


**The classes breakdown as such:**

1. TopSort.py -> This class is responsible for using topological sort to take the adjacency list/edge list and output an array representing papers with the most citations and least citations amongst themselves. In effect, newer papers build upon the foundational knowledge of the papers they cite. The class is also responsible for writing the final sorting order onto a csv file, referencing a map to reconstruct the Research Rabbit Id's from shorter normalized IDs. The Research Rabbit IDs are used to source the paper's information from the input csv file.
2. Main.py -> This class is responsible for taking in the citation graph exported from Research Rabbit, converting the csv into an edge list, then converting the edge list to an adjacency list and finally ordering the edge list and adjacency list. The final reading order is written onto a csv file for permanent storage (Rather than being stored in memory).
3. Graph_conversion.py -> This file is responsible for taking in the input csv file, building pairs to represent edges (Citing,Cited), and finally parsing the edge list in the build_edges function. The build_edges function can rebuild the edge list to reverse the order of pairs (Cited,Citing), and normalize the long Research Rabbit IDs into shorter values like P1 and P2 (Better hashing performance with adjacency lists). The build_edges function also returns a reverse map, which can reconvert the normalized IDs back into the Research Rabbit IDs.
4. adjacency_builder.py -> This class takes the edge lists created by the graph_conversion file and creates adjacency lists, as well as verifying the adjacency list is acyclic. The verification process is the most important part of this class, as topological sort simply does not work with graphs that contain cycles.

**How Topological Sorting Works**

We are using Kahn's algorithm which uses Breadth First Search (Queues) to sort a list of unordered list of nodes with dependencies. The algorithm hinges on the number of in-degrees for each node (Ie the number of incoming edges). 0 in-degrees means this node has no previous nodes it depends upon. In the context of this project, we instead use out-degrees (Outgoing edge from a node) to represent the number of papers that cite this particular paper ex) Paper B: [Paper A, Paper X] means paper B is cited by Paper A and Paper X. We use out-degrees for the sorted list to order the final list as Foundational Papers->Newer Papers.
  
  For each cited paper (key), each citing paper's out-degree is increased by one (This paper has one more outgoing edge). If a node does not cite any other paper, it will have an outdegree of 0. The algorithm starts by calculating the out-degrees and adding nodes with an out-degree of 0 to the queue. This means, the queue starts filled with Papers that are not citing anything (Not dependant/building upon another paper's knowledge). 
  
  The program then performs a breadth first search, popping the nodes in the queues and looking through the papers that cite this particular paper. Since the parent node was popped, the out-degrees for each connected node is decreased by one (There is one less outgoing edge). If a child node has an out-degree of 0, it can be added to the queue as paper it depends on has already been "read". This process of popping nodes in the queue and looking through connected nodes is repeated until there are no nodes remaining.
  
**Analysis**
-time complexity, if we encountered errors, how the performance differs across a hdd over an ssd. 

**Topological Sort Class**

Adjacency List:
- Setting up the in-degrees for the adjacency list is an O(n+m) procedure where N represents the keys, and M represents the values/edges for the dictionary.
- Searching for in-degree=0 is an O(n) operation, all of the nodes are iterated through.
- The BFS iteration is also O(n+m), every key(n) is iterated through once and each edges(m) is accessed by popping the key node.
- The final time compexity is O(n+m)

Edge List:
- To find the in-degrees(incoming edges) for each pair(m), the time complexity is O(m).
- To find nodes(n) with no incoming edges is O(n).
- The BFS iteration is O(n*m), the algorithm looks at every node(n) in the queue and looks through the pairs(m) to find associated edges.
- The final time complexity is O(m*n)

Verify List:
- To verify the sort, the program has to iterate through each node (n) in the adjacency list, and the connected node(m).
- The time complexity is O(n+m)

Create File:
  - This function is O(n^2) as the function iterates through every node(n) in the sorted list, and finds the associated node in the csv to extract the information for storage.

**Time Measurements**

For each of the following, Tests were run 10 times per each measurement.

Time it takes to create Lists
(SSD)
- Reversing Map + ID: 0.0095 < x < 0.0190
- Reversing Map: 0.0095 < x < 0.0195
- No Reversing Map, No ID Map: 0.0098 < x < 0.0157

Time it takes to sort Edge Lists
- Reversing At End, No ID map: 1.731*e^-5 < x < 2.473*e^-5
- Reversed List Prior, No ID map: 1.6099*e^-5 < x < 2.2700*e^-5
- Reversed List prior, ID Map: 1.580*e^-5 < x < 2.239*e^-5

Time it takes to sort Adjacency Lists
- Reversing At End, No ID map: 1.379*e^-5 < x < 2.079*e^-5
- Reversed List Prior, no ID map: 1.3099*e^-5 < x < 1.8600*e^-5
- Reversed List prior, ID Map: 1.269*e^-5 < x < 1.889*e^-5

References:
GeeksforGeeks. (2025, October 31). Topological sorting using BFS - Kahn’s algorithm. https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/ 
