from rest_framework import serializers

from variables.models import Variable


class VariableListSerializer(serializers.ModelSerializer):
    entity = serializers.StringRelatedField()

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
        ]
        depth = 0


class VariableDetailSerializer(serializers.ModelSerializer):
    entity = serializers.StringRelatedField()
    # dependencies = serializers.StringRelatedField(many=True)

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
            "dependencies",
        ]
        depth = 2