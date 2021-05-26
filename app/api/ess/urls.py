from django.urls import path
from . import views

urlpatterns = [
    path("activity_NABERS/", views.Activity_NABERS.as_view()),
]
