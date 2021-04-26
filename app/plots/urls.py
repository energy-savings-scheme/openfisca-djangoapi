from django.urls import path
from plots.views import BarChart_id, BarChart_alias, NetworkGraph_shortest

urlpatterns = [
    path("id", BarChart_id),
    path("alias", BarChart_alias),
    path("shortest/<str:var_id>", NetworkGraph_shortest)
]
