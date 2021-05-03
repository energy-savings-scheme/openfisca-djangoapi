from plots.plots import varIDBarChart, variable_directory
from plots.network_graph import network_graph
from django.shortcuts import render


def BarChart_id(request):
    context = {'plot': varIDBarChart('id')}
    response = render(request, 'plots/barchart.html', context)
    return response


def BarChart_alias(request):
    context = {'plot': varIDBarChart('alias')}
    response = render(request, 'plots/barchart.html', context)
    return response


def Directory_Map(request):
    context = {'plot': variable_directory()}
    response = render(request, 'plots/barchart.html', context)
    return response


def NetworkGraph_shortest(request, var_id):
    """
    # GET dependency network graph of a single Variable

    # Returns
    - html directed graph for all children of a variable
        with the shortest path length as layout algorithm

    # URL parameter (required)
    The following url parameter must be specified
    - variable_name [str]: e.g. "/shortest/<variable_name>

    """
    context = {'plot': network_graph(var_id, layout='shortest')}
    response = render(request, 'plots/barchart.html', context)
    return response
