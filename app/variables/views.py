from django.utils import timezone

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from config.pagination import LargeResultsSetPagination
from variables.models import FormulaVariable, Variable
from variables.serializers import VariableListSerializer, VariableChildrenSerializer


class VariablesList(generics.ListAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    pagination_class = LargeResultsSetPagination


class VariableDetail(generics.RetrieveAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"


class VariableChildrenList(generics.RetrieveAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableChildrenSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"