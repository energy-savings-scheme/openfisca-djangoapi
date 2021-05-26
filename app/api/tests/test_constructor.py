from django.test import TestCase

from api.constructor import OpenFiscaAPI_BaseView

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

    # def test_get_dependencies_method(self):
    #     base = OpenFiscaAPI_BaseView(variable_name="test_variable")
    #     dependencies = base.get_dependencies()

    #     assert isinstance(dependencies, list)
    #     assert self.child_variable in dependencies