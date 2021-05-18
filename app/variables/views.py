# from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import generics, filters
# from rest_framework.response import Response
# from rest_framework.views import APIView


from config.pagination import LargeResultsSetPagination
from variables.models import Variable
from variables.serializers import VariableListSerializer, VariableChildrenSerializer


class VariablesList(generics.ListAPIView):
    """
    # LIST all Variables stored in the database

    # Returns
    - array of Variable objects (JSON)

    # Query params (optional)
    This endpoint accept the following query params:
    - search [str]: e.g "/variables?search=abc"
    - is_output [bool]: e.g. "/variables?is_output=true"
    - is_input [bool]: e.g. "/variables?is_input=true"
    - majorcat [str]: e.g "/variables?majorcat=E"
    - minorcat [str]: e.g "/variables?minorcat=E1"

    Multiple queries can be combined with "&" (for example: "/variables?search=abc&is_final=true")

    """

    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer

    def get_queryset(self):
        query_set = Variable.objects.all()
        is_output = self.request.query_params.get("is_output", None)
        is_input = self.request.query_params.get("is_input", None)
        majorCat = self.request.query_params.get("majorcat", None)
        minorCat = self.request.query_params.get("minorcat", None)
        schedule = self.request.query_params.get("schedule", None)
        activity = self.request.query_params.get("activity", None)

        if is_input is not None:
            if is_input.lower() == "false":
                query_set = query_set.annotate(num_parents=Count("children")).filter(
                    num_parents__gt=0
                )
            else:
                query_set = query_set.annotate(num_parents=Count("children")).filter(
                    num_parents=0
                )

        if is_output is not None:
            if is_output.lower() == "false":
                query_set = query_set.annotate(num_children=Count("parents")).filter(
                    num_children__gt=0
                )
            else:
                query_set = query_set.annotate(num_children=Count("parents")).filter(
                    num_children=0
                )

        if majorCat is not None:
            query_set = query_set.filter(metadata__majorCat=majorCat)

        if minorCat is not None:
            query_set = query_set.filter(metadata__minorCat=minorCat)

        if schedule is not None:
            query_set = query_set.filter(
                Q(
                    metadata__regulation_reference__part__part_type="Schedule",
                    metadata__regulation_reference__part__identifier=schedule,
                )
                | Q(
                    metadata__regulation_reference__part__part__part_type="Schedule",
                    metadata__regulation_reference__part__part__identifier=schedule,
                )
            )

        if activity is not None:
            query_set = query_set.filter(
                Q(
                    metadata__regulation_reference__part__part__part_type="Activity Definition",
                    metadata__regulation_reference__part__part__identifier=activity,
                )
                | Q(
                    metadata__regulation_reference__part__part_type="Activity Definition",
                    metadata__regulation_reference__part__identifier=activity,
                )
            )

        # print(query_set.count())
        return query_set

    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description"]


class VariableDetail(generics.RetrieveAPIView):
    """
    # GET details of a single Variable

    # Returns
    - a Variable object (JSON)
    - or a 404 error if the specified Variable could not be found

    # URL parameter (required)
    The following url parameter must be specified
    - variable_name [str]: e.g. "/variables/<variable_name>/

    """

    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"


class VariableChildrenList(generics.RetrieveAPIView):
    """
    # GET dependency tree of a single Variable

    # Returns
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

    # URL parameter (required)
    The following url parameter must be specified
    - variable_name [str]: e.g. "/variables/<variable_name>/children/

    """

    queryset = Variable.objects.all()
    serializer_class = VariableChildrenSerializer
    lookup_field = "name"
    lookup_url_kwarg = "variable_name"
