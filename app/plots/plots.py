import numpy as np
import plotly.graph_objects as go
from plotly.io import to_html
import networkx as nx


from variables.models import Variable
from django.db.models import Count


def varIDBarChart(name='alias'):

    var_names = []
    var_alias = []
    parents_number = []
    children_number = []

    for entry in Variable.objects.all():
        var_names.append(entry.name)
        var_alias.append(entry.metadata['alias'])
        parents_number.append(entry.parents.count())
        children_number.append(entry.children.count())

    if (name == 'id'):
        display_name = var_names
        display_height = 11000
    elif(name == 'alias'):
        display_name = var_alias
        display_height = 9000

    trace1 = go.Bar(y=display_name,
                    x=parents_number,
                    orientation='h',
                    name="parents",
                    marker=dict(
                        color='#fb743e'
                    ),
                    # TODO: onHover: display var_id
                    )
    trace2 = go.Bar(y=display_name,
                    x=children_number, orientation='h', name="children",
                    marker=dict(
                        color='#8ac4d0'),

                    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack',
        width=1300,
        height=display_height,
        yaxis=dict(
            categoryorder='total ascending',
            showticklabels=True,
            dtick=1,
            tickangle=0,
            tickfont=dict(family='serif',
                          size=12,
                          color='#28527a',
                          ),
            # tickmode='array',
            # tickvals=np.arange(start=0, stop=848, step=1),
            # ticktext=var_alias),)
        ),
        xaxis=dict(
            mirror=True,  # TODO: try with bigger top margin
            showticklabels=True,
            dtick=2,
            tick0=0,
        ),
        paper_bgcolor='#f7f6e7',
        plot_bgcolor='rgba(0,0,0,0)',
        # plot_bgcolor='#314e52'

    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)
    return plot_div


def graph():

    G = nx.random_geometric_graph(200, 0.125)
    edge_x = []

    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
        title='<br>Network graph made with Python',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        annotations=[dict(
            text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002)],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )
    plot_div = fig.to_html(full_html=False)
    return plot_div
