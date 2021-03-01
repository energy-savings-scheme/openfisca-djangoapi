from django.urls import path, re_path, include

from variables.views import ExampleView

urlpatterns = [
    path('example_abc/', ExampleView.as_view()),
]
