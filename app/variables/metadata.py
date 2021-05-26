import re
from django.db.models import Count, Q
from plots.network_graph import get_variable_graph
import networkx as nx


def makeAlias(name0):
    aliasList = []
    for word in name0.split("_"):
        if word.isupper():
            aliasList.append(word)
        else:
            aliasList.append(word.title())

    alias = " ".join(aliasList)

    return alias


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


def regulation_ref(metadata):
    """
    helper function to create activity entry by unpacking the regulation reference from openfisca variables
    """
    # metadata = entry.metadata
    if (metadata != None):
        if "regulation_reference" in metadata.keys():

            ref = entry.metadata["regulation_reference"]
            reg_ref = {"version_name": ref['version'],
                       "version_code": ref['identifier']}
            while "part" in ref.keys():
                ref = ref["part"]
                if (ref["part_type"] == "SubMethod"):
                    reg_ref["subMethod"] = ref["title"]

                if (ref["part_type"] == "Activity Definition"):
                    reg_ref["activity"] = ref["title"]

                if (ref["part_type"] == "Requirement"):
                    if ref["identifier"] == "energy_savings":
                        reg_ref["energy_savings"] = True
                    elif ref["identifier"] == "implementation":
                        reg_ref["implementation"] = True
                    elif ref["identifier"] == "eligibility":
                        reg_ref["eligibility"] = True
                    elif ref["identifier"] == "equipment":
                        reg_ref["equipment"] = True

            return reg_ref
