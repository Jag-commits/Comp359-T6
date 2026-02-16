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
