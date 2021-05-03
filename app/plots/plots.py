import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.io import to_html
import networkx as nx
import plotly.express as px


from variables.models import Variable
from django.db.models import Count

colorScheme = {
    "background_color": 'rgba(0, 0, 0, 0)',
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


def variable_directory():
    """
    this plots the directory map of all variables in the code base
    """
    # TODO: put it into the right data frame

    var_id = []
    var_alias = []
    scheme_name = []
    method_name = []
    file_name = []
    file_var_count = []

    for entry in Variable.objects.all():
        var_id.append(entry.name)
        var_alias.append(entry.metadata['alias'])
        directory_list = entry.directory.split("/")
        if (directory_list[0] == 'variables'):
            scheme_name.append(directory_list[1])

        if (directory_list[-1].endswith('.py')):
            file_name.append(directory_list[-1])

        if (len(directory_list) == 4):
            method_name.append(directory_list[2])
        else:
            method_name.append(directory_list[-1].split(".py")[0])

    df = pd.DataFrame(data={
        'var_id': var_id,
        'alias': var_alias,
        'scheme': scheme_name,
        'method': method_name,
        'file': file_name,
    })
    df.reset_index()
    file_counts = df['file'].value_counts()
    print(file_counts['Fridge_specific_variables.py'])
    df1 = df.groupby(by='method').agg('count')
    print(df1)

    fig = px.treemap(
        df, path=['scheme', 'method', 'file'], color_continuous_scale='RdBu', color_continuous_midpoint='10',
        height=700, width=1500)

    # fig.update_layout(uniformtext=dict(minsize=10, mode='hide'))

    plot_div = fig.to_html(full_html=False)
    return plot_div
