from variables.models import Variable
import networkx as nx
import plotly.graph_objects as go
from plotly.io import to_html
import numpy as np
from networkx.utils import pairwise
import itertools


# TODO: save all children in cache
# https://docs.djangoproject.com/en/3.1/ref/models/querysets/#prefetch-related

Variable.objects.all().prefetch_related('children')


def get_variable_graph(var_id, G):
    """
    Returns all children nodes and directed edge for the
        maximum depth.
    This is used for drawing network graph
        for the children variables
    """

    try:
        variable = Variable.objects.get(name=var_id)
        var_type = variable.metadata['variable-type']
        G.add_node(var_id, type=var_type)

        if (variable.children.count() != 0):
            for child in variable.children.all():
                G.add_edge(var_id, child.name)
                get_variable_graph(child.name, G)
                print(".")

        return G

    except Variable.DoesNotExist:
        print(f"{var_id} does not exist")
        return None


def get_all_children(var_id, node_list, edge_list, attribute_list):
    """
    Returns all children nodes and directed edge for the
        maximum depth.
    This is used for drawing network graph
        for the children variables
    """

    try:
        variable = Variable.objects.get(name=var_id)
        node_list.append(var_id)
        attribute_list.append(variable.metadata['variable-type'])

        if (variable.children.count() != 0):
            for child in variable.children.all():
                edge = (var_id, child.name)
                edge_list.append(edge)
                get_all_children(child.name, node_list,
                                 edge_list, attribute_list)
                print(".")

        print('----------------')

        print(attribute_list)
        print(node_list)

        return dict(nodes=node_list, edges=edge_list, attributes=attribute_list)

    except Variable.DoesNotExist:
        print(f"{var_id} does not exist")
        return None


def test_graph():
    t = np.linspace(0, 10, 100)
    y = np.sin(t)
    test_trace = go.Scatter(
        x=t, y=y, mode="markers"
    )
    fig = go.Figure(data=[test_trace])
    plot_div = fig.to_html(full_html=False)
    return plot_div


def graph(G):

    node_list = G.nodes
    edge_list = G.edges
    # G = nx.DiGraph()
    # G.add_nodes_from(node_list, type=attribute_list)
    # G.add_edges_from(edge_list)
    # print(G.nodes(data=True))
    seed = 13425
    # spring_layout or spiral_layout is good for lots of nodes
    # planar or shell is good for small number of nodes
    # TODO: with multiplartitle_layout using subsets of (output, intermediatory, input)

    pos = nx.spiral_layout(G)

    var_id = node_list[0]
    var_id_x, var_id_y = pos[var_id]
    var_id_trace = go.Scatter(
        x=[var_id_x], y=[var_id_y],
        mode='markers',
        hoverinfo='text',
        text=var_id,
        marker=dict(size=16, color='#fb743e', symbol='square')
    )

    node_x = []
    node_y = []
    node_name = []

    for node in G.nodes:
        node_name.append(node)
        x0, y0 = pos[node]
        node_x.append(x0)
        node_y.append(y0)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_name,
        marker=dict(size=16, color='#8ac4d0')
    )

    edge_x = []
    edge_y = []
    for edge in G.edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
    )

    layout = go.Layout(
        title=f"{var_id}",
        height=800,
        width=800,
        showlegend=False,
        paper_bgcolor='#f7f6e7',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)

    )

    # TODO: print out the number of nodes present
    # TODO: node size corresponds to adjacency size

    fig = go.Figure(data=[edge_trace, node_trace, var_id_trace], layout=layout)
    plot_div = fig.to_html(full_html=False)
    return plot_div


def multipartiteGraph(G):
    print(G.nodes(data=True))
    pos = nx.multipartite_layout(G, subset_key="subset", align='horizontal')
    print(pos)


def network_graph():
    var_id = 'F1_5_meets_installation_requirements'
    # var_id = "office_maximum_electricity_consumption"
    # var_id = "number_of_certificates"
    G = nx.DiGraph()
    H = get_variable_graph(
        var_id, G)
    for node, varType in H.nodes(data=True):
        if varType == 'input':
            G.nodes[node]['subset'] = 0
        elif varType == 'output':
            G.nodes[node]['subset'] = 2
        else:
            G.nodes[node]['subset'] = 1
    print(H.nodes(data=True))
    # return graph(H)
    multipartiteGraph(H)
