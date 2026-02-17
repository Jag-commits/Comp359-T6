# we are not using get_refernce_pairs for the final submission, hardcoded edges are there only for testing.
# def get_reference_pairs():
#     """
#     Returns the citation pairs in the form:
#         (NewPaper, ReferencedPaper)
#     """
#     return [
#         ("Cavalcante, 2016", "Nassirtoussi, 2015"),
#         ("Cavalcante, 2016", "Tkac, 2016"),
#         ("Sutskever, 2014", "Auvolat, 2016"),
#         ("Lee, 2019", "Han, 2019"),
#         ("Rundo, 2019", "Lee, 2019"),
#         ("Rundo, 2019", "Sutskever, 2014"),
#         ("Rundo, 2019", "Cavalcante, 2016"),
#     ]



# This file converts citation data from ResearchRabbit into
# a directed graph that can be used for topological sorting.
# The idea is simple:
# If Paper C cites Paper A, then there is a relation C -> A.
# But if we want a reading schedule, we usually reverse it
# so A comes before C.


import csv


# Load citation data from CSV
# CSV format should be:
# new,ref
# PaperC,PaperA

def clean_name(name):
    if name is None:
        return ""
    return " ".join(name.strip().split())

def load_citation_data(file_name):
    pairs = []

    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            new_paper = clean_name(row["new"])
            ref_paper = clean_name(row["ref"])

            if new_paper and ref_paper:
                pairs.append((new_paper, ref_paper))

    return pairs



def assign_ids(papers):
    papers = sorted(set(papers))
    id_map = {}
    reverse_map = {}

    for i, paper in enumerate(papers):
        pid = "P" + str(i + 1)
        id_map[paper] = pid
        reverse_map[pid] = paper

    return id_map, reverse_map

def build_edges(pairs, reverse=False, use_ids=False):
    # collect all paper names first
    all_names = []
    for a, b in pairs:
        all_names.extend([a, b])
    
    id_map, reverse_map = {}, {}
    if use_ids:
        id_map, reverse_map = assign_ids(all_names)
    
    edges = []
    for new_paper, ref_paper in pairs:
        # get id if using ids, otherwise use name
        u = id_map.get(new_paper, new_paper)
        v = id_map.get(ref_paper, ref_paper)
        
        if reverse:
            # reverse direction for reading order (ref -> new)
            edges.append((v, u))
        else:
            # citation direction (new -> ref)
            edges.append((u, v))
    
    return edges, id_map, reverse_map

# build adjacency list from edges
# edge (u, v) means u points to v
def build_graph(edges):
    graph = {}
    for u, v in edges:
        # make sure both nodes exist in graph
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
    return graph

#what to do ??
#Convert citation data into directed graph (entry point for Sorting Team)
# ResearchRabbit: file path (CSV) or list of (new, ref) citation pairs
# Returns graph (adjacency list), edge_list, id_map, reverse_map
# Edge direction: if C cites A then edge is (C, A) so dependencies are correct
def graphBuilder(ResearchRabbit):
    if isinstance(ResearchRabbit, str):
        pair = load_citation_data(ResearchRabbit)
    else:
        pairs = [(clean_name(a), clean_name(b)) for a, b in ResearchRabbit]
        pairs = [(a, b) for a, b in pairsif a and b]
    edges, id_map, reverse_map = build_edges(pairs, reverse=False, use_ids=False)
    graph = build_graph(edges)
    return graph, edges, id_map, reverse_map

## temporary part##
def make_schedule(order, per_week=3):
    schedule = []
    current_week=[]
    for paper in order:
        current_week.append(paper)

        if len(current_week) == per_week:
            schedule.append(current_week)
            current_week=[]
    # now add the remaining papers
     if len(current_week)>0:
        schedule.append(current_week)
        return schedule
