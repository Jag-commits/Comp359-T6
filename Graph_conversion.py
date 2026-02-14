# graph_conversion.py
# -------------------
# This file contains the citation graph I got from ResearchRabbit.
#
# IMPORTANT:
# ResearchRabbit direction (as described):
#   (NewPaper, ReferencedPaper)
# Meaning:
#   NewPaper used ReferencedPaper as a reference.
#
# For a reading schedule (topological sort):
#   You should read ReferencedPaper BEFORE NewPaper.
# So we convert each pair into an edge:
#   ReferencedPaper -> NewPaper

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


