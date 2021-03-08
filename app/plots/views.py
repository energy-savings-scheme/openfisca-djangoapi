from . import plots
from django.views.generic.base import TemplateView
from django.shortcuts import render


# TODO: API endpoint /barchart0 for a bar chart listing all variables with their number of children and parents


def BarChart(request):
    context = {'plot': plots.plot1d}
    response = render(request, 'plots/barchart.html', context)
    return response
