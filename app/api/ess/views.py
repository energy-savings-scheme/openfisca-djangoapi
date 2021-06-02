from rest_framework.response import Response

from api.views import OpenFiscaAPI_BaseView
from variables.models import Variable


class ESS__D16__deemed_elec_savings(OpenFiscaAPI_BaseView):
    variable_name = "ESS__D16__deemed_elec_savings"


class ESS__number_of_ESCs(OpenFiscaAPI_BaseView):
    variable_name = "ESS__number_of_ESCs"