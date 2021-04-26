import distutils.util

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from variables.models import Variable


class VariableListSerializer(serializers.ModelSerializer):
    entity = serializers.StringRelatedField()
    children = serializers.StringRelatedField(many=True)
    parents = serializers.StringRelatedField(many=True)
    default_value = serializers.SerializerMethodField()

    class Meta:
        model = Variable
        fields = [
            "name",
            "description",
            "directory",
            "value_type",
            "entity",
            "definition_period",
            "default_value",
            "possible_values",
            "metadata",
            "formula",
            "children",
            "parents",
        ]
        depth = 0

    def get_default_value(self, obj):
        if obj.value_type == "Int":
            return int(obj.default_value)

        if obj.value_type == "Float":
            return float(obj.default_value)

        if obj.value_type == "Boolean":
            return bool(distutils.util.strtobool(obj.default_value))

        return obj.default_value


class VariableChildrenSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Variable
        fields = [
            "name",
            "children",
        ]
