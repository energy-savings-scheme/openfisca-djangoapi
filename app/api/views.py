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
        print(serializer.data)

        self.perform_create(serializer)
        print("AFTER CALLING PERFORM")
        print(serializer.data)
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
        payload = {
            "buildings":
            {
                "building_1":
                {
                    "AC_has_5_years_warranty": {"2021-05-31": True},
                    "Air_Conditioner__cooling_capacity": {"2021-05-31": 3.5},
                    'Air_Conditioner_type': {'2021-05-31': "type_6"},
                    'Appliance__installation_purpose': {'2021-05-31': "residential"},
                    'Appliance__installation_type': {'2021-05-31': "replacement"},
                    'Appliance__zone_type': {'2021-05-31': "average"},
                    'Appliance_demand_response_capability': {'2021-05-31': True},
                    'Appliance_is_installed': {'2021-05-31': True},
                    'Appliance_is_registered_in_GEMS': {'2021-05-31': True},
                    'Appliance_is_removed': {'2021-05-31': True},
                    'Appliance_located_in_residential_building': {'2021-05-31': False},
                    'No_Existing_AC': {'2021-05-31': False},
                    'PDRS_AC_power_input': {'2021-05-31': 0.765},
                    'PDRS_HEAB_AC_replace_peak_demand_savings': {'2021-05-31': None},
                    'implementation_is_performed_by_qualified_person': {'2021-05-31': True}
                },
            },
            'persons': {
                'person1': {}
            }
        }

        print(payload)

        try:
            resp = requests.post(
                f"{settings.OPENFISCA_API_URL}/calculate/", json=payload
            )
        except Exception as e:
            raise APIException(
                {
                    "error": "An error occurred while making the request to the OpenFisca API!",
                    "message": str(e),
                }
            )

        print(resp.status_code)

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
            print(resp.text)

        return resp.text
