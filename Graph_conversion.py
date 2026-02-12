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

def get_reference_pairs():
    """
    Returns the citation pairs in the form:
        (NewPaper, ReferencedPaper)
    """
    return [
        ("Cavalcante, 2016", "Nassirtoussi, 2015"),
        ("Cavalcante, 2016", "Tkac, 2016"),
        ("Sutskever, 2014", "Auvolat, 2016"),
        ("Lee, 2019", "Han, 2019"),
        ("Rundo, 2019", "Lee, 2019"),
        ("Rundo, 2019", "Sutskever, 2014"),
        ("Rundo, 2019", "Cavalcante, 2016"),
    ]
