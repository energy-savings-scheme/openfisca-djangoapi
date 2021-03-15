from variables.models import Variable
import networkx as nx


def get_all_children(var_id, node_list, edge_list):
    """
    Returns all children nodes and directed edge for the
        maximum depth.
    This is used for drawing network graph
        for the children variables
    """
    # node_list = []
    # edge_list = []
    try:
        variable = Variable.objects.get(name=var_id)
        node_list.append(var_id)
        print(variable.name)

        if (variable.children.count() != 0):
            for child in variable.children.all():
                edge = (var_id, child.name)
                edge_list.append(edge)
                get_all_children(child.name, node_list, edge_list)
                print(".")

        print('----------------')

        return dict(nodes=node_list, edges=edge_list)

    except Variable.DoesNotExist:
        print(f"{var_id} does not exist")
        return None


def graph(node_list, edge_list):
    G = nx.DiGraph()
    G.add_nodes_from(node_list)
    G.add_edges_from(edge_list)
    print(G.nodes)
    print(G.edges)
