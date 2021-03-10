from django.urls import path

from plots.views import BarChart_id, BarChart_alias, Graph

urlpatterns = [
    path("id", BarChart_id),
    path("alias", BarChart_alias),
    path("graph", Graph)
]
