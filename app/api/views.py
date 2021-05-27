from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        """This function performs the following:
        i) collects the POST request data
        ii) validates the data according to the Serializer validation rules
            - e.g. checks that BooleanFields are boolean, and CharFields are strings...
        iii) performs whatever business-logic we want to do
        iv) returns a Response to the user

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """This function is where we perform our business logic (i.e. call the OpenFisca `POST /calculate` endpoint)
            - we want to update `serializer.data` with the calculated response.

        NOTE - you can access the validated data using `serializer.validated_data`
        """

        # TODO - implement OpenFisca API call here. Steps:
        #  i) Construct the payload for the OpenFisca `POST /calculate/` request.
        #     - this needs to be in the correct format with all the correct entities and names etc. (see https://openfisca.org/doc/openfisca-web-api/input-output-data.html)
        # ii) Make POST request to `https://{openfisca_api_url}/calculate/`

        print(serializer.validated_data)
        return None
