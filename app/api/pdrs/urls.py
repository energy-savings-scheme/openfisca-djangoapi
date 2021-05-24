from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path("activity_x1/", views.activity_x1),
]
