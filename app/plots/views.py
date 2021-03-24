from plots.plots import varIDBarChart
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


def Graph(request):
    context = {'plot': network_graph()}
    response = render(request, 'plots/barchart.html', context)
    return response
