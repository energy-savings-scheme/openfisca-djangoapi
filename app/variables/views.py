from django.utils import timezone

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from config.pagination import LargeResultsSetPagination
from variables.models import Variable
from variables.serializers import VariableListSerializer, VariableDetailSerializer


class VariablesList(generics.ListAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    pagination_class = LargeResultsSetPagination


class VariableDetail(generics.RetrieveAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableDetailSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"