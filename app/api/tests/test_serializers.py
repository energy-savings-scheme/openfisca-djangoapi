from django.test import TestCase

from api.serializers import OpenFiscaAPI_BaseSerializer

from variables.models import Variable


class TestOpenFiscaAPI_BaseSerializer(TestCase):
    def setUp(self):
        self.child_variable = Variable.objects.create(name="child_variable")
        self.variable = Variable.objects.create(
            name="test_variable", metadata={"input_offspring": ["child_variable"]}
        )

    def test_instantiating_serializer_without_specifying_variable_raises_AttributeError(
        self,
    ):
        with self.assertRaises(AttributeError):
            invalid = OpenFiscaAPI_BaseSerializer()

    def test_get_dependencies_method(self):
        serializer = OpenFiscaAPI_BaseSerializer(variable=self.variable)
        dependencies = serializer.get_dependencies()

        assert isinstance(dependencies, list)
        assert self.child_variable in dependencies