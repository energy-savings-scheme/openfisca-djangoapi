from django.utils import timezone
from django.db.models import Count, Q

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

    def get_queryset(self):
        # query_set = Variable.objects.filter(
        #     Q(name__icontains="nabers") | Q(description__icontains="nabers"))
        # print(len(query_set))
        query_set = Variable.objects.all()

        # Check for the query params: `is_output` and `is_input`
        # If those query params don't exist, we just ignore it and move on...
        is_output = self.request.query_params.get("is_output", None)
        is_input = self.request.query_params.get("is_input", None)

        if is_output is not None:
            # `query_set.annotate` will perform some arithmetic on the Queryset, so we can do some smarter filtering
            # Here we annotate the number of `parents` each variable has...
            query_set = query_set.annotate(num_parents=Count("children")).filter(
                num_parents=0
            )

        if is_input is not None:
            # `query_set.annotate` will perform some arithmetic on the Queryset, so we can do some smarter filtering
            # Here we annotate the number of `children` each variable has...
            query_set = query_set.annotate(num_children=Count("is_parent")).filter(
                num_children=0
            )

        # And finally return the filtered Queryset to be sent in the Response
        return query_set

    filter_backends = [filters.SearchFilter]
    search_fields = ["$name", "$description"]


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
