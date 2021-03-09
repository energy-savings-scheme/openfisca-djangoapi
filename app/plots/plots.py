import numpy as np
import plotly.graph_objects as go
from plotly.io import to_html
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
                    x=parents_number, orientation='h', name="parents", marker=dict(
                        color='#fb743e',),
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
            mirror=True,
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
