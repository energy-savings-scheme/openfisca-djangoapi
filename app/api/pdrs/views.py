from rest_framework.response import Response

from api.views import OpenFiscaAPI_BaseView
from variables.models import Variable


class Activity_x1(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_AC_firmness_factor"
