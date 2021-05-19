from variables.models import Variable
import networkx as nx
import plotly.graph_objects as go
from plotly.io import to_html
import numpy as np
from networkx.utils import pairwise
from networkx.algorithms.shortest_paths.unweighted import single_source_shortest_path_length
import itertools
from plots.plots import colorScheme

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
        aliasList = variable.metadata['alias'].split(" ")
        if (len(aliasList) >= 5):
            alias = " ".join(aliasList[0:5])
        else:
            alias = variable.metadata['alias']
        G.add_node(var_id, type=var_type, alias=alias)

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
                G.nodes[node]['subset'] = 2
            elif varType['type'] == 'output':
                G.nodes[node]['subset'] = 0
            elif varType['type'] == 'intermediary':
                G.nodes[node]['subset'] = 1
            else:
                G.nodes[node]['subset'] = -1

        pos = nx.multipartite_layout(
            G, subset_key="subset", align='horizontal')
    elif layout == "planar":
        pos = nx.planar_layout(G)
    elif layout == "spring":
        pos = nx.spring_layout(G)
    elif layout == "shell":
        pos = nx.shell_layout(G)
    elif layout == "spiral":
        pos = nx.spiral_layout(G)
    else:
        pos = nx.spiral_layout(G)

    return pos


def graph(var_id, G, layout="shortest"):
    # summary info on the network
    main_node = G.nodes[var_id]['alias']

    # node_list = list(G.nodes)
    # edge_list = list(G.edges)

    pos = display_pos(G, layout)

    var_id_x, var_id_y = pos[var_id]
    var_id_trace = go.Scatter(
        x=[var_id_x], y=[var_id_y],
        mode='markers+text',
        hoverinfo='text',
        text=main_node,
        textposition="middle right",
        textfont=dict(
            size=14,
            color=colorScheme['text_color']
        ),
        marker=dict(
            size=25, color=colorScheme['trace1_color'], symbol='square')
    )

    node_x = []
    node_y = []
    node_name = []
    node_color = []
    node_size = []
    node_symbol = []
    for node, data in G.nodes(data=True):
        if data['type'] == 'input':
            node_name.append(data['alias'])
            node_color.append(colorScheme['trace2_color'])
            node_size.append(25)
            node_symbol.append('diamond')
        elif data['type'] == 'output':
            node_name.append(None)
            node_color.append(colorScheme['trace1_color'])
            node_size.append(25)
            node_symbol.append('square')
        else:
            node_name.append(data['alias'])
            node_color.append(colorScheme['highlight_color'])
            node_size.append(25)
            node_symbol.append('circle')

        x0, y0 = pos[node]
        node_x.append(x0)
        node_y.append(y0)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        hoverinfo='text',
        text=node_name,
        textposition="middle center",
        textfont=dict(
            size=13,
            color=colorScheme['text_color']
        ),
        marker=dict(size=node_size, color=node_color, symbol=node_symbol),
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
        line=dict(width=1, color=colorScheme['trace2_color']),
        hoverinfo='none',
    )
    node_size_total = G.number_of_nodes()
    edge_size_total = G.number_of_edges()

    layout = go.Layout(
        title=f'{main_node}\n' f'({node_size_total} nodes & {edge_size_total} edges)',
        height=900,
        width=1200,
        showlegend=False,
        paper_bgcolor=colorScheme['background_color'],
        plot_bgcolor=colorScheme['background_color'],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    # TODO: show direction (through color of edges?)

    fig = go.Figure(data=[edge_trace, node_trace,
                          var_id_trace], layout=layout)
    plot_div = fig.to_html(full_html=False)

    return plot_div


def network_graph(var_id, layout):

    G = nx.DiGraph()
    H = get_variable_graph(
        var_id, G)

    return graph(var_id, H, layout)
