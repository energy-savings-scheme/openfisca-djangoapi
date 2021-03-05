from django.urls import path, re_path, include

from variables.views import VariablesList, VariableDetail

urlpatterns = [
    path("", VariablesList.as_view()),
    path("<str:variable_name>/", VariableDetail.as_view()),
]
