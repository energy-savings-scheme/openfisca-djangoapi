<<<<<<< HEAD
from rest_framework import generics
=======
from django.utils import timezone
from django.db.models import Count, Q

from rest_framework import generics, filters
>>>>>>> 12ecf77f5f18779970508fb8fb64bca0ca80e342
from rest_framework.response import Response
from rest_framework.views import APIView


from config.pagination import LargeResultsSetPagination
from variables.models import FormulaVariable, Variable
from variables.serializers import VariableListSerializer, VariableChildrenSerializer


class VariablesList(generics.ListAPIView):
    """
    ## LIST all Variables stored in the database

    ### Returns
    - array of Variable objects (JSON)

    ### Query params (optional)
    This endpoint accept the following query params:
    - search [str]: e.g "/variables?search=abc"
    - is_final [bool]: e.g. "/variables?is_final=true"

    Multiple queries can be combined with "&" (for example: "/variables?search=abc&is_final=true")

    """

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
    """
    ## GET details of a single Variable

    ### Returns
    - a Variable object (JSON)
    - or a 404 error if the specified Variable could not be found

    ### URL parameter (required)
    The following url parameter must be specified
    - variable_name [str]: e.g. "/variables/<variable_name>/

    """

    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"


class VariableChildrenList(generics.RetrieveAPIView):
    """
    ## GET dependency tree of a single Variable

    ### Returns
    - a tree structure (in JSON format) recursively listing each child of the specified Variable, and each of <em>that variable's</em> children, etc.
    - or a 404 error if the specified Variable could not be found
    - the structrue of the tree is:
        ```python
        {  name: "abc",
            children: [
                        {name: "def" , children: [ ... ]},
                        {name: "ghi" , children: [ ... ]},
                      ]
        }
        ```

    ### URL parameter (required)
    The following url parameter must be specified
    - variable_name [str]: e.g. "/variables/<variable_name>/children/

    """

    queryset = Variable.objects.all()
    serializer_class = VariableChildrenSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"
