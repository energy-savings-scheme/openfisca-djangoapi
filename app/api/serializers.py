from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from variables.models import Variable


class OpenFiscaAPI_BaseSerializer(ModelSerializer):
    """This is a sublass of ModelSerializer. The intent is to automatically create
    a serializer with Fields for each input/output related to the Parent variable
    """

    def __init__(self, *args, **kwargs):
        self.variable = kwargs.get("variable")
        super().__init__()

    def get_dependencies(self):
        # Return list of `Variable` objects which are `input_offspring` of `self.variable`
        dependencies_list = self.variable.metadata.get("input_offspring", [])

        return [Variable.objects.get(name=dep) for dep in dependencies_list]

    def get_fields(self):
        """Return the dict of field names -> field instances that should be
        used for `self.fields` when instantiating the serializer.

        There should be one field for each `input_offspring` of the Variable.
        """

        # NOTE - this is currently incomplete! It currently always just returns a "ChoiceField".
        # What we want is to return the correct Field type based on the `Variable.value_type`
        return {
            dependency.name: serializers.ChoiceField(
                choices=["red", "green", "blue"], style={"base_template": "radio.html"}
            )
            for dependency in self.get_dependencies()
        }
