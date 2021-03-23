from variables.models import Variable
import networkx as nx
import plotly.graph_objects as go
from plotly.io import to_html
import numpy as np
from networkx.utils import pairwise
from networkx.algorithms.shortest_paths.unweighted import single_source_shortest_path_length
import itertools


# TODO: just a thought: can I pull all variables into a graph instead. Is it even possible? There would be clusters, which could be the automatic categories. i.e. we categorise by dependencies instead of guessing through var names and description.


# TODO: check if I am using it the right way, particularly trying to get variable data
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

        return G

    except Variable.DoesNotExist:
        print(f"{var_id} does not exist")
        return None


def display_pos(G, layout='shortest'):
    ''' Display Position of the Nodes:
    # spiral

    # 1. general layout that works well for lots of nodes
     # pos = nx.spiral_layout(G)

    # "variable-type":
        multiplartitle_layout using subsets of (output, intermediatory, input). it works well for small number of nodes, but not for a bigger set of nodes


    # "shortest" by default
        multiplartitle_layout using shortest distance to the source.
    '''
    if layout == 'shortest':
        var_id = list(G.nodes)[0]
        shortest_length = single_source_shortest_path_length(G, var_id)

        for node in shortest_length.keys():
            G.nodes[node]['shortest'] = shortest_length[node]

        pos = nx.multipartite_layout(
            G, subset_key="shortest", align='horizontal')

    elif layout == "variable-type":
        for node, varType in G.nodes(data=True):
            if varType['type'] == 'input':
                G.nodes[node]['subset'] = 0
            elif varType['type'] == 'output':
                G.nodes[node]['subset'] = 2
            elif varType['type'] == 'intermediary':
                G.nodes[node]['subset'] = 1
            else:
                G.nodes[node]['subset'] = -1

        pos = nx.multipartite_layout(
            G, subset_key="subset", align='horizontal')
    else:
        pos = nx.spiral_layout(G)

    return pos


def graph(G):

    node_list = list(G.nodes)
    edge_list = list(G.edges)
    seed = 13425

    # TODO: color by type of nodes (output, inter, input)
    pos = display_pos(G)
    var_id = list(G.nodes)[0]

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

    # TODO: print out some general state of a network: number of nodes, number of edges,
    # TODO: node color/size corresponds to adjacency size
    # TODO: show direction (through color of edges?)

    fig = go.Figure(data=[edge_trace, node_trace, var_id_trace], layout=layout)
    plot_div = fig.to_html(full_html=False)
    return plot_div


def network_graph():
    var_id = 'F1_5_meets_installation_requirements'
    # var_id = "office_maximum_electricity_consumption"
    # var_id = "number_of_certificates"
    # var_id = "number_of_apartments"
    G = nx.DiGraph()
    H = get_variable_graph(
        var_id, G)

    print(H.edges(data=True))

    return graph(H)
