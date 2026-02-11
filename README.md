COMP 349, ON 1 Assignment 2 README 

*Analysis Framework*

Independent Variables

Dependent Variables

Evaluation Method

Failure Conditions
	-Missing Nodes/Papers in the topological sorting output.

Constraints
	-Nodes are limited to <=8 Papers.
Design Decisions
	- The algorithm uses adjacency lists as opposed to a 2d matrix. This is because 2d arrays require the program to iterate through each of the sub arrays to determine which nodes are connected to other nodes, leading to O(n^2) time complexity. Adjacency lists, as dictionaries can store the connected nodes, meaning the program just needs to iterate through the key value pairs leading to O(n+m) time complexiy.
	-The topological sort ordering is based on the most number of in-degrees(Incoming edges/incoming citations) to least number of in-degrees. This is ordering is the reverse of the traditional topological sorting output. The algorithm reverses the ordering, since the newer papers build off of the knowledge from previous papers. 
The classes breakdown as such:


	1. TopSort.py -> This class is responsible for using topological sort to take the adjacency list and output an array representing papers with the most citations and least citations amongst themselves. In effect, newer papers build upon the foundational knowledge of the papers they cite.
	2. Main.py -> This class is responsible for taking in the citation graph exported from Research Rabbit, converting the list to an edge list, then converting the edge list to an adjacency list and finally ordering the papers for the user.

