from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.constructor import OpenFiscaAPI_BaseView
from variables.models import Variable


class Activity_x1(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_AC_firmness_factor"
