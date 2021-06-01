import datetime

from rest_framework import serializers

from variables.models import Variable


def get_serializer_field_for_variable(variable, write_only=False, read_only=False):
    """Helper function that returns the correct Serializer Field for a Variable.
    The 'correct' field will depend on the `Variable.value_type` attribute, according
    to the mapping below:
        - "Int" -> serializers.IntegerField
        - "Float" -> serializers.FloatField
        - "Boolean" -> serializers.BooleanField
        - "String" -> serializers.CharField
        - "Date" -> serializers.DateField
        - "Enum" -> serializers.ChoiceField
    """

    if variable.value_type == "Int":
        return serializers.IntegerField(
            default=variable.default_value,
            read_only=read_only,
            write_only=write_only,
            help_text=variable.description,
        )
    elif variable.value_type == "Float":
        return serializers.FloatField(
            default=variable.default_value,
            read_only=read_only,
            write_only=write_only,
            help_text=variable.description,
        )
    elif variable.value_type == "Boolean":
        return serializers.BooleanField(
            default=variable.default_value,
            read_only=read_only,
            write_only=write_only,
            help_text=variable.description,
        )
    elif variable.value_type == "String":
        return serializers.ChoiceField(
            choices=variable.possible_values,
            default=variable.default_value,
            read_only=read_only,
            write_only=write_only,
            help_text=variable.description,
        )
    elif variable.value_type == "Date":
        return serializers.DateField(
            default=variable.default_value,
            read_only=read_only,
            write_only=write_only,
            help_text=variable.description,
        )
    # elif variable.value_type == "Enum":
    #     return serializers.CharField(
    #         default="NOT IMPLEMENTED YET",
    #         read_only=read_only,
    #         write_only=write_only,
    #         help_text=variable.description,
    #     )
    else:
        raise Exception(
            f"Cannot find corresponding Serializer Field for variable: {variable.name}"
        )


class OpenFiscaAPI_BaseSerializer(serializers.Serializer):
    """This is a sublass of ModelSerializer. The intent is to automatically create
    a serializer with Fields for each input/output related to the Parent variable
    """

    def __init__(self, *args, **kwargs):
        self.variable = kwargs.pop("variable", None)
        if not self.variable:
            raise AttributeError(
                "The attribute `variable` must be specified when instantiating this serializer!"
            )
        super().__init__(*args, **kwargs)

    def get_dependencies(self):
        # Return list of `Variable` objects which are `input_offspring` of `self.variable`
        dependencies_list = self.variable.metadata.get("input_offspring", [])

        return [Variable.objects.get(name=dep) for dep in dependencies_list]

    def get_fields(self):
        """Return the dict of field names -> field instances that should be
        used for `self.fields` when instantiating the serializer.

        There should be one field for each `input_offspring` of the Variable.
        """

        fields = {
            dependency.name: get_serializer_field_for_variable(
                dependency, write_only=True
            )
            for dependency in self.get_dependencies()
        }
        fields["period"] = serializers.DateField(
            default=datetime.date.today, write_only=True
        )
        fields[self.variable.name] = get_serializer_field_for_variable(
            self.variable,
            read_only=True,
        )

        return fields
