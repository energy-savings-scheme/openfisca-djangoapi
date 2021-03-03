from django.utils import timezone
from django.db.models import Q

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView


from config.pagination import LargeResultsSetPagination
from variables.models import FormulaVariable, Variable
from variables.serializers import VariableListSerializer, VariableChildrenSerializer


class VariablesList(generics.ListAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    # pagination_class = LargeResultsSetPagination

    # TODO: retrieve variables with no parents
    # TODO: retrieve variables with no children

    # def get_queryset(self):
    #     query_set = Variable.objects.filter(
    #         Q(name__icontains="nabers") | Q(description__icontains="nabers"))
    #     print(len(query_set))
    #     return query_set

    filter_backends = [filters.SearchFilter]
    search_fields = ['$name', '$description']


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
