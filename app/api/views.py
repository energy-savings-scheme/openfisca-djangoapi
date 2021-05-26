from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from api.serializers import OpenFiscaAPI_BaseSerializer
from variables.models import Variable


class OpenFiscaAPI_BaseView(CreateAPIView):
    serializer_class = OpenFiscaAPI_BaseSerializer
    variable_name = None

    def __init__(self, **kwargs):
        # Get the Variable object specified in `variable_name`.
        # Raise Exception if no matching Variable found.
        if kwargs.get("variable_name"):
            self.variable_name = kwargs.get("variable_name")
        try:
            self.variable = Variable.objects.get(name=self.variable_name)
        except Variable.DoesNotExist as e:
            raise e

        # Then run the `__init__` method of the parent class "APIView"
        super().__init__(**kwargs)

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs.setdefault("variable", self.variable)
        return serializer_class(*args, **kwargs)