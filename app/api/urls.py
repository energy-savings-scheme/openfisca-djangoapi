from django.urls import include, path

urlpatterns = [
    path("ess/", include(("api.ess.urls", "ess"), namespace="ess")),
    path("pdrs/", include(("api.pdrs.urls", "pdrs"), namespace="pdrs")),
]
