from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api.views import OpenFiscaAPI_BaseView
from api.pdrs.views import PDRS_HEAB_AC_replace_peak_demand_savings

from variables.models import Variable


class TestOpenFiscaAPI_Base(TestCase):
    def setUp(self):
        self.child_variable = Variable.objects.create(name="child_variable")
        self.variable = Variable.objects.create(
            name="test_variable", metadata={"input_offspring": ["child_variable"]}
        )

    def test_init_method(self):
        # Test init method for valid variable
        valid = OpenFiscaAPI_BaseView(variable_name="test_variable")
        # Test init method raises Exception for invalid variable
        with self.assertRaises(Variable.DoesNotExist):
            invalid = OpenFiscaAPI_BaseView(variable_name="invalid_variable")


class Test_View_PDRS_ROOA_fridge_peak_demand_savings(TestCase):
    def setUp(self):
        offsprings = [
            "ESS__method_type",
            "ESS__NABERS_type_of_creation",
            "ESS__postcode",
            "ESS__NABERS_benchmark_elec_consumption",
            "ESS__NABERS_NABERS_electricity",
            "ESS__NABERS_onsite_unaccounted_electricity",
            "ESS__NABERS_counted_electricity_savings",
        ]
        for offspring in offsprings:
            Variable.objects.create(name=offspring, value_type="Boolean")

        self.variable = Variable.objects.create(
            name="PDRS_HEAB_AC_replace_peak_demand_savings",
            value_type="Boolean",
            metadata={"input_offspring": offsprings},
        )

    def test_post_request(self):
        factory = APIRequestFactory()
        request = factory.post(
            "/some_url/",
            {
                "ESS__method_type": True,
                "ESS__NABERS_type_of_creation": "true",
                "ESS__postcode": 0,
                "ESS__NABERS_benchmark_elec_consumption": 0,
                "ESS__NABERS_NABERS_electricity": 0,
                "ESS__NABERS_onsite_unaccounted_electricity": 0,
                "ESS__NABERS_counted_electricity_savings": 0,
                "period": "2021-05-27",
            },
        )
        res = PDRS_HEAB_AC_replace_peak_demand_savings.as_view()(request)

        assert res.status_code == 201