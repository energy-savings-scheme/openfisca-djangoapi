from django.urls import path, re_path, include

from entities.views import EntitiesList

urlpatterns = [
    path("", EntitiesList.as_view()),
]
