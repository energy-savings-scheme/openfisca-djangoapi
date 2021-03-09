from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from variables.models import Variable


class VariableListSerializer(serializers.ModelSerializer):
    entity = serializers.StringRelatedField()
    children = serializers.StringRelatedField(many=True)
    parents = serializers.StringRelatedField(many=True)

    # children = serializers.StringRelatedField(source="get_children", many=True)
    # parents = serializers.StringRelatedField(source="get_parents", many=True)

    class Meta:
        model = Variable
        fields = [
            "name",
            "description",
            "value_type",
            "entity",
            "definition_period",
            "default_value",
            "possible_values",
            "metadata",
            "children",
            "parents",
        ]
        depth = 0


class VariableChildrenSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Variable
        fields = [
            "name",
            "children",
        ]
