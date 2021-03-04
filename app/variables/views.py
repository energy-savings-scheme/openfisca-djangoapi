from django.utils import timezone
from django.db.models import Count, Q

from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView


from config.pagination import LargeResultsSetPagination
from variables.models import FormulaVariable, Variable
from variables.serializers import VariableListSerializer, VariableChildrenSerializer


# TODO: allow different wordings
def update_categories(majorCat, minorCat):
    entries = Variable.objects.select_for_update().filter(
        Q(name__icontains=minorCat) | Q(description__icontains=minorCat))
    entries.update(metadata={'majorCat': majorCat, 'minorCat': minorCat})


variableTree = {
    'resa': ['resa'],    # RESA: Recognised Energy Savings Activity
    'nabers': ['nabers'],
    'D': ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', ],
    'E': ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13'],
    'F': ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15'],
}


def updateByVariableTree():
    for key in variableTree:
        majorCat = key
        for subCat in variableTree[key]:
            update_categories(majorCat, subCat)


class VariablesList(generics.ListAPIView):
    """
    # LIST all Variables stored in the database

    # Returns
    - array of Variable objects (JSON)

    # Query params (optional)
    This endpoint accept the following query params:
    - search [str]: e.g "/variables?search=abc"
    - is_final [bool]: e.g. "/variables?is_final=true"
    - majorcat [str]: e.g "/variables?majorcat=E"
    - minorcat [str]: e.g "/variables?majorcat=E1"

    Multiple queries can be combined with "&" (for example: "/variables?search=abc&is_final=true")

    """

    queryset = Variable.objects.all()
    serializer_class = VariableListSerializer
    # pagination_class = LargeResultsSetPagination

    # updateByVariableTree()

    # Variable.objects.filter(metadata__minorCat='resa').update(
    #     metadata={'majorCat': 'resa', 'minorCat': 'resa'})

    def get_queryset(self):
        query_set = Variable.objects.all()
        is_output = self.request.query_params.get("is_output", None)
        is_input = self.request.query_params.get("is_input", None)
        majorCat = self.request.query_params.get("majorcat", None)
        minorCat = self.request.query_params.get("minorcat", None)

        if is_output is not None:
            query_set = query_set.annotate(
                num_parents=Count("children")).filter(num_parents=0)

        if is_input is not None:
            query_set = query_set.annotate(
                num_children=Count("is_parent")).filter(num_children=0)

        if majorCat is not None:
            query_set = query_set.filter(metadata__majorCat=majorCat)

        if minorCat is not None:
            query_set = query_set.filter(metadata__minorCat=minorCat)

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
