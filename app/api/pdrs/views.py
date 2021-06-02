from rest_framework.response import Response

from api.views import OpenFiscaAPI_BaseView
from variables.models import Variable


class PDRS_ROOA_fridge_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_ROOA_fridge_peak_demand_savings"



class PDRS_HEER_AC_replace_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_HEER_AC_replace_peak_demand_savings"

class PDRS_HEER_AC_install_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_HEER_AC_install_peak_demand_savings"



class PDRS_HEAB_AC_replace_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_HEAB_AC_replace_peak_demand_savings"

class PDRS_HEAB_AC_install_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_HEAB_AC_install_peak_demand_savings"



class PDRS_HEAB_motors_replace_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_HEAB_AC_replace_peak_demand_savings"

class PDRS_HEAB_motors_install_peak_demand_savings(OpenFiscaAPI_BaseView):
    variable_name = "PDRS_HEAB_AC_install_peak_demand_savings"

