from django.urls import path
from . import views

urlpatterns = [
    path("D16_deemed_electricity_savings/", views.ESS__D16__deemed_elec_savings.as_view()),
    path("NABERS_number_of_ESCs/", views.ESS__number_of_ESCs.as_view()),
]
