import json
import requests

from django.conf import settings

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView


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

        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            response, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """This function is where we perform our business logic (i.e. call the OpenFisca `POST /calculate` endpoint)
            - we want to update `serializer.data` with the calculated response.

        NOTE - you can access the validated data using `serializer.validated_data`
        """

        userInput = serializer.validated_data

        period = userInput["period"]
        del userInput["period"]
        userInput[self.variable_name] = None
        payload_user = {}
        for key in userInput.keys():
            payload_user[key] = {str(period): userInput[key]}

        payload_base = {
            "buildings": {
                "building_1": payload_user},
            "persons": {
                "person1": {}
            }
        }

        try:
            resp = requests.post(
                f"{settings.OPENFISCA_API_URL}/calculate/", json=payload_base
            )
        except Exception as e:
            raise APIException(
                {
                    "error": "An error occurred while making the request to the OpenFisca API!",
                    "message": str(e),
                }
            )

        # Handle OpenFisca `400: Bad Request` error
        if resp.status_code == 400:
            raise ValidationError(
                {
                    "error": " (400) An error occurred during the OpenFisca calculation!",
                    "message": json.loads(resp.text),
                }
            )

        # Handle OpenFisca `500: Server Error` error
        if resp.status_code == 500:
            raise APIException(
                {
                    "error": "(500) An error occurred during the OpenFisca calculation!",
                    "message": json.loads(resp.text),
                }
            )

        # Handle other non-success responses:
        if resp.status_code not in [200, 201]:
            raise APIException(
                {
                    "error": "(not in 200, 201) An error occurred during the OpenFisca calculation!",
                    "message": json.loads(resp.text),
                }
            )

        # Finally - handle success!
        if resp.status_code in [200, 201]:
            response = resp.json()
            return response['buildings']['building_1']
