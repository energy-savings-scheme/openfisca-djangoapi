import numpy as np
import pandas as pd
import plotly.graph_objects as go
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
    offspring_number = []

    for entry in Variable.objects.filter(name__icontains='PDRS'):
        var_names.append(entry.name)
        var_alias.append(entry.metadata['alias'])
        parents_number.append(entry.parents.count())
        children_number.append(entry.children.count())
        offspring_number.append(len(entry.metadata['input_offspring']))

    if (name == 'id'):
        display_name = var_names
        display_height = len(var_names) * 30
    elif(name == 'alias'):
        display_name = var_alias
        display_height = len(var_alias) * 30

    trace1 = go.Bar(x=display_name,
                    y=children_number,
                    # orientation='h',
                    name="children",
                    text=children_number,
                    textposition="auto",
                    marker=dict(
                        color=colorScheme['trace1_color']
                    ),
                    # TODO: onHover: display var_id
                    )
    trace2 = go.Bar(x=display_name,
                    y=parents_number,
                    text=parents_number,
                    textposition="inside",
                    # orientation='h',
                    name="parents",
                    marker=dict(
                        color=colorScheme['trace2_color']),

                    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack',
        width=1500,
        height=display_height,
        yaxis=dict(
            showticklabels=False,
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
            categoryorder='total descending',
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
    # file_var_count = []

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

    df_var = pd.DataFrame(data={
        'var_id': var_id,
        'alias': var_alias,
        'scheme': scheme_name,
        'method': method_name,
        'file': file_name,
    })
    df_var.reset_index()
    # file_counts = df_var['file'].value_counts()

    # df1 = df_var.groupby(by='method').agg('count')

    fig = px.treemap(
        df_var, path=['scheme', 'method', 'file'],
        color='scheme',
        color_discrete_map={
            '(?)': colorScheme['highlight_color'],
            'General_Appliances': colorScheme['trace2_color'], 'Home_Energy_Efficiency_Retrofits (HEER)': colorScheme['trace2_color'],
            'High_Efficiency_Appliances_Business (HEAB)': colorScheme['trace2_color'],
            'Other_ESS_methods': colorScheme['trace1_color'], 'Removal_of_Old_Appliances (RoOA)': colorScheme['trace2_color']},
        title="Overview of Openfisca_nsw_safeguard Code Base",
        height=700, width=1500)

    fig.update_layout(uniformtext=dict(minsize=14, mode='hide'))
    plot_div = fig.to_html(full_html=False)
    return plot_div
