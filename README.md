COMP 359, ON 1 Assignment 2 README 

Responsibility Split: https://docs.google.com/document/d/1CNVFqzEXJpOW_nXpOcXWMrRaES8_cz77Pl4NT2S9Sik/edit?usp=sharing 

The goal was to create an implementation of topological sort that would generate a viable reading schedule for a Research Rabbit export. Some measurements were gathered to evaluate which approach to the implementation is the most efficient, results are evaluated at the end.

**Notes**
1. The Research Rabbit (Pushpdeep's) export represents 8 papers covering the topic of machine learning. Various prerequisite papers are used to build upon the knowledge for the paper, Francesco Rundo (2019).
2. Any other Research Rabbit csv file must have the columns: DOI, Title, Year, ResearchRabbitId, PrereqIds

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
- The sorted list is compared to the new verification method to ensure pre-requisite papers are in the sorted list prior to the papers that cite them.
  
Evaluation Method
- The citation graph csv is loaded into memory
- The citation csv is first converted into an edgelist.
- Each edge is mapped into an adjacency list and checked for cycles
- The final sorted list is sent through the baseline to ensure it's in a valid order.
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

1. TopSort.py -> This class is responsible for using topological sort to take the adjacency list/edge list and output an array representing papers with the most citations and least citations amongst themselves. In effect, newer papers build upon the foundational knowledge of the papers they cite. The class is also responsible for writing the final sorting order onto a csv file, referencing a map to reconstruct the Research Rabbit Id's from shorter normalized IDs. The Research Rabbit IDs are used to source the paper's information from the input csv file. The class also contains a verification function to ensure pre-requisite papers were read before the newer papers.
2. Main.py -> This class is responsible for taking in the citation graph exported from Research Rabbit, converting the csv into an edge list, then converting the edge list to an adjacency list and finally ordering the edge list and adjacency list. The final reading order is written onto a csv file for permanent storage (Rather than being stored in memory).
3. Graph_conversion.py -> This file is responsible for taking in the input csv file, building pairs to represent edges (Citing,Cited), and finally parsing the edge list in the build_edges function. The build_edges function can rebuild the edge list to reverse the order of pairs (Cited,Citing), and normalize the long Research Rabbit IDs into shorter values like P1 and P2 (Better hashing performance with adjacency lists). The build_edges function also returns a reverse map, which can reconvert the normalized IDs back into the Research Rabbit IDs.
4. adjacency_builder.py -> This class takes the edge lists created by the graph_conversion file and creates adjacency lists, as well as verifying the adjacency list is acyclic. The verification process is the most important part of this class, as topological sort simply does not work with graphs that contain cycles.

**How Topological Sorting Works**

We are using Kahn's algorithm which uses Breadth First Search (Queues) to sort a list of unordered list of nodes with dependencies. The algorithm hinges on the number of in-degrees for each node (Ie the number of incoming edges). 0 in-degrees means this node has no previous nodes it depends upon. In the context of this project, we instead use out-degrees (Outgoing edge from a node) to represent the number of papers that cite this particular paper ex) Paper B: [Paper A, Paper X] means paper B is cited by Paper A and Paper X. We use out-degrees for the sorted list to order the final list as Foundational Papers->Newer Papers.
  
  For each cited paper (key), each citing paper's out-degree is increased by one (This paper has one more outgoing edge). If a node does not cite any other paper, it will have an outdegree of 0. The algorithm starts by calculating the out-degrees and adding nodes with an out-degree of 0 to the queue. This means, the queue starts filled with Papers that are not citing anything (Not dependant/building upon another paper's knowledge). 
  
  The program then performs a breadth first search, popping the nodes in the queues and looking through the papers that cite this particular paper. Since the parent node was popped, the out-degrees for each connected node is decreased by one (There is one less outgoing edge). If a child node has an out-degree of 0, it can be added to the queue as paper it depends on has already been "read". This process of popping nodes in the queue and looking through connected nodes is repeated until there are no nodes remaining.

**Input and Output CSV Files**

The input file, consisting of the aforementioned 8 papers, is sourced from Research Rabbit's citation graph. Prerequisite's/Connections were built manually as Research Rabbit does not provide the edges/connection data.

The final sorted file consists of the DOI, Year, Title, Link-> The link in particular is useful for referencing these papers at a later point in time.

To ensure the list was sorted 100% correctly, the file was manually checked. 

The Sorted Order: Han (2019), Auvolat (2006), Nassirtoussi (2015), Tkac (2016), Lee (2019), Sutskever (2014), Cavalcante (2016), Rundo (2019)

Note: Sutskever (2014) cites Auvolat (2016), which would be logically impossible. However, this publication date seems to be an error on the part of Research Rabbit as the paper has conflicting dates when viewed in the map (2016) and list (2015).
Based on research, the actual date is 2006: https://scholar.google.com/citations?view_op=view_citation&hl=fr&user=QWCHPhMAAAAJ&citation_for_view=QWCHPhMAAAAJ:zYLM7Y9cAGgC.

**Analysis**
-time complexity and how the performance differs across a hdd over an ssd. 

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
- The program has to find the index location for each node (n) and connected node (m) while looping through nodes in the adjacency list. Meaning this part is O(n^2)
- The time complexity is O(n^2)

Create File:
  - This function is O(n^2) as the function iterates through every node(n) in the sorted list, and finds the associated node in the csv to extract the information for storage.

**Time Measurements**

For each of the following, Tests were run 10 times per each measurement.
Time it takes to create Lists, Measured in Seconds

(HDD)
- No Reverse Map, no IDs: 0.000202 < x < 0003629  
Mean: 0.00024578  SD: 6.684e-05
- Reversed List, No IDs: 0.0001852 < x < 0002682  
Mean: 0.0002028  SD: 2.459e-05
- Reversed List, IDs: 0001912 < x < 0002592  
Mean: 0.0002072  SD: 2.321e-05
  
(NVME SSD)
- No Reversing Map, No ID Map: 0.000218 < x < 000288  
Mean: 0.000236  SD: 1.914e-05 
- Reversing Map, No IDs: 0.000220 < x < 0.000297  
Mean: 0.000237  SD: 2.386e-05
- Reversing Map + ID: 0.000230 < x < 0.000299  
Mean: 0.000239  SD: 2.268e-05

Time it takes to sort Edge Lists
- Reversing At End, No ID map: 5.2000e-06 < x < 8.7000e-06  
Mean: 6.6300e-06  SD: 1.4086e-06    
- Reversed List Prior, No ID map: 5.3000e-06 < x < 9.9000e-06  
Mean: 5.9800e-06  SD: 6.126e-07 
- Reversed List prior, ID Map: 5.2000e-06 < x < 6.1000e-06  
Mean: 5.4100e-06  SD: 3.0710e-07 

Time it takes to sort Adjacency Lists
- Reversing At End, No ID map: 4.0000e-06 < x < 7.4000e-06  
Mean: 4.9400e-06  SD: 1.2367e-06 
- Reversed List Prior, no ID map: 4.0000e-06 < x < 7.7000e-06  
Mean: 4.5400e-06  SD: 1.1228e-06 
- Reversed List prior, ID Map: 3.8000e-06 < x < 4.5000e-06  
Mean: 4.1500e-06  SD: 2.1730e-07

From the evidence, the results seem to suggest reversing the list with an ID map has genuine benefits over the older implementation of reversing the final sorted list with Research Rabbit IDs. Reversing the list through [::-1] has an additional time complexity of O(n). This could explain why starting with a reversed list is consistently faster than without, as the algorithm doesn't need to spend additional time reversing the order of nodes. The ID maps provided a slight advantage over the Research Rabbit IDs. This could be because the long RRabbit ID strings could have reduced the hashing performance for looking up a key in the adjacency list. The edge list implementation could be seeing an improvement with the ID system because of the comparison checks looking for matching node names (Eg if pair[0] == firstNode). Since the node names are drastically shorter, the comparisons are less expensive. As for the time taken to generate the lists, there seems to be no noticeable impact from using an SSD over a HDD. This is likely because the file is so small, any difference in reading speeds is miniscule compared to the CPU overhead to read and store the data in memory. There also seems to be an unnoticeable difference in the time taken for additional steps like reversing or adding an ID map to the list. These additions may happen incredibly quickly, and they won't show up in rounded results.

Overall, for the purposes of generating a viable reading schedule, normalizing IDs for each node and reversing the list (Cited->Citing) prior to sorting provides considerable performance uplifts with unnoticeable performance degredation in list creation.

Vlog Jagpreet: https://drive.google.com/file/d/1nR8qNyfJjg-_TDoSD-GFVF1stXQ0fdpN/view?usp=sharing 

Vlog Pushpdeep: https://www.youtube.com/watch?v=Cwitf_hmUZM

Vlog Jang Toor: https://youtu.be/f6MdI_mH4k8

References:

Research Rabbit Collection Link (Thanks to Pushpdeep): https://app.researchrabbit.ai/folder-shares/5a40ab39-9b72-4d2c-9fee-18fcdfc63cf9

Khapra, S. (2025, October 2). Topological Sorting in Graph | using DFS | Lecture 117 [Video]. YouTube. https://www.youtube.com/watch?v=0WIINUY12Yg

Stapleton, A. (2024, March 5). How To Use Research Rabbit - Effortlessly Explore Literature for FREE! [Video]. YouTube. https://www.youtube.com/watch?v=phWqcGcxeE4

GeeksforGeeks. (2025, October 31). Topological sorting using BFS - Kahn’s algorithm. https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/ 

Hogg, G. (2024, July 18). Graphs: Edge List, Adjacency Matrix, Adjacency List, DFS, BFS - DSA Course in Python Lecture 11 [Video]. YouTube. https://www.youtube.com/watch?v=4jyESQDrpls

Kindson The Genius. (2021, September 18). Part 8 - What is the Adjacency List or Matrix [Video]. YouTube. https://www.youtube.com/watch?v=l3aLJIM9RGo

ness-intricity101. (2021, November 11). What is DAG? [Video]. YouTube. https://www.youtube.com/watch?v=1Yh5S-S6wsI


