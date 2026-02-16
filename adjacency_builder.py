class adjacency_builder:
    def adjacencyBuilder(edgelist, all_nodes=None):

        adj = {}

        # Ensure every node exists
        if all_nodes is not None:
            for n in all_nodes:
                adj.setdefault(n, [])

        for paper, prereq in edgelist:
            adj.setdefault(paper, [])
            adj.setdefault(prereq, [])

            # avoid duplicates
            if prereq not in adj[paper]:
                adj[paper].append(prereq)

        return adj

    def is_dag(adj):
        # Using DFS colors to detect a cycle in a directed graph.

        # WHITE=unvisited, GRAY=visiting (in stack), BLACK=finished
        WHITE, GRAY, BLACK = 0, 1, 2  

        # starting by marking every node as WHITE (unvisited)
        color = {node: WHITE for node in adj}  

        def dfs(u):
            # If anyone is entering node u, so I mark it as GRAY it’s now in my recursion stack.
            color[u] = GRAY

            # We checked every neighbor v that u points to u to v
            for v in adj.get(u, []):
                # If v is GRAY, we found a back-edge to a node still in my stack to cycle
                if color.get(v, WHITE) == GRAY:
                    return False

                if color.get(v, WHITE) == WHITE:
                    # If the deeper DFS finds a cycle, do we immediately return False upward.
                    if not dfs(v):
                        return False

            # If we finish exploring all neighbors of u with no cycle, I mark u as BLACK which means fully done
            color[u] = BLACK

            # Returning True means: no cycle was found starting from u
            return True

        # run DFS from every node which covers disconnected components.
        for node in adj:
            # If we haven’t visited this or certain node yet, then we start a DFS from it.
            if color[node] == WHITE:
                # If that DFS finds a cycle, the whole graph is not a DAG.
                if not dfs(node):
                    return False

        # If all DFS runs finish without finding a cycle, then the graph is a DAG.
        return True
