from rest_framework.response import Response

from api.views import OpenFiscaAPI_BaseView
from variables.models import Variable


class Activity_NABERS(OpenFiscaAPI_BaseView):
    variable_name = "ESS__electricity_savings"
