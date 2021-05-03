from variables.models import Variable
from django.db.models import Count, Q
from plots.network_graph import get_variable_graph
import networkx as nx


def variableType(entry):
    if entry.parents.count() == 0 and entry.children.count() > 0:
        if entry.metadata is None:
            entry.metadata = {"variable-type": "output"}
        else:
            entry.metadata["variable-type"] = "output"
    elif entry.children.count() == 0 and entry.parents.count() > 0:
        if entry.metadata is None:
            entry.metadata = {"variable-type": "input"}
        else:
            entry.metadata["variable-type"] = "input"
    elif entry.children.count() == 0 and entry.parents.count() == 0:
        if entry.metadata is None:
            entry.metadata = {"variable-type": "orphan"}
        else:
            entry.metadata["variable-type"] = "orphan"
    else:
        if entry.metadata is None:
            entry.metadata = {"variable-type": "intermediary"}
        else:
            entry.metadata["variable-type"] = "intermediary"
    entry.save()


def get_input_offsprings(entry):
    # NOTE (RP) -> the `nx.DiGraph` function is very slow and probably not necessary.
    #               I would suggest instead recursively searching through 'children'
    #               until you've reached the bottom of the tree.
    input_offsprings = []
    G = nx.DiGraph()
    H = get_variable_graph(entry.name, G)
    for node, nodeAttr in H.nodes(data=True):
        if nodeAttr["type"] == "input":
            input_offsprings.append(node)

    entry.metadata["input_offspring"] = input_offsprings
    entry.save()
