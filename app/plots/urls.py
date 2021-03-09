from django.urls import path

from plots.views import BarChart_id, BarChart_alias

urlpatterns = [
    path("id", BarChart_id),
    path("alias", BarChart_alias),

]
