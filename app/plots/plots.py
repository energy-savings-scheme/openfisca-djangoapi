import numpy as np
import plotly.graph_objects as go
from plotly.io import to_html
import networkx as nx


from variables.models import Variable
from django.db.models import Count

colorScheme = {
    "background_color": '#eeebdd',
    "trace1_color": "#913535",
    "trace2_color": "#283148",
    "text_color": "#283148",
    "highlight_color": "#8ea6b4",
}


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
        display_height = len(var_names) * 20
    elif(name == 'alias'):
        display_name = var_alias
        display_height = len(var_alias) * 20

    trace1 = go.Bar(y=display_name,
                    x=parents_number,
                    orientation='h',
                    name="parents",
                    marker=dict(
                        color=colorScheme['trace1_color']
                    ),
                    # TODO: onHover: display var_id
                    )
    trace2 = go.Bar(y=display_name,
                    x=children_number, orientation='h', name="children",
                    marker=dict(
                        color=colorScheme['trace2_color']),

                    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack',
        width=1000,
        height=display_height,
        yaxis=dict(
            categoryorder='total ascending',
            showticklabels=True,
            dtick=1,
            tickangle=0,
            tickfont=dict(family='serif',
                          size=12,
                          color=colorScheme['text_color'],
                          ),
        ),
        xaxis=dict(
            mirror=True,  # TODO: try with bigger top margin
            showticklabels=True,
            dtick=1,
            tick0=0,
        ),
        paper_bgcolor=colorScheme['background_color'],
        plot_bgcolor=colorScheme['background_color'],

    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = fig.to_html(full_html=False)
    return plot_div
