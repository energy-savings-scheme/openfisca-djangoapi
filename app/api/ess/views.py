from drf_spectacular.utils import extend_schema
from rest_framework.response import Response

from api.views import OpenFiscaAPI_BaseView
from variables.models import Variable

@extend_schema(description="""Calculates the `deemed electricity savings` achieved under
                              Activity D16 of the Energy Savings Scheme. 
                              This value is used in Equation 1 to determine the number of ESCs created.""")
class ESS__D16__deemed_elec_savings(OpenFiscaAPI_BaseView):
    variable_name = "ESS__D16__deemed_elec_savings"

@extend_schema(description="""Calculates the number of `Energy Savings Certificates (ESCs)` created under
                              the Energy Savings Scheme (ESS). This value corresponds to Equation 1 in the ESS.""")
class ESS__number_of_ESCs(OpenFiscaAPI_BaseView):
    variable_name = "ESS__number_of_ESCs"