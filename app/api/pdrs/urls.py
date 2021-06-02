from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path("ROOA_fridge_peak_demand_savings/", views.PDRS_ROOA_fridge_peak_demand_savings.as_view()),

    path("HEER_AC_replace_peak_demand_savings/", views.PDRS_HEER_AC_replace_peak_demand_savings.as_view()),
    path("HEER_AC_install_peak_demand_savings/", views.PDRS_HEER_AC_install_peak_demand_savings.as_view()),

    path("HEAB_AC_replace_peak_demand_savings/", views.PDRS_HEAB_AC_replace_peak_demand_savings.as_view()),
    path("HEAB_AC_install_peak_demand_savings/", views.PDRS_HEAB_AC_install_peak_demand_savings.as_view()),

    path("HEAB_motors_replace_peak_demand_savings/", views.PDRS_HEAB_motors_replace_peak_demand_savings.as_view()),
    path("HEAB_motors_install_peak_demand_savings/", views.PDRS_HEAB_motors_install_peak_demand_savings.as_view()),

]
