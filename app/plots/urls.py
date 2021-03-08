from django.urls import path

from plots.views import BarChart

urlpatterns = [
    path("", BarChart)
]
