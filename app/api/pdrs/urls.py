from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path("activity_x1/", views.Activity_x1.as_view()),
]
