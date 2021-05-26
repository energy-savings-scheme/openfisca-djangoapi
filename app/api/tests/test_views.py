from django.test import TestCase

from api.serializers import OpenFiscaAPI_BaseSerializer
from api.views import OpenFiscaAPI_BaseView

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
