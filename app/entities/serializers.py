from rest_framework import serializers

from entities.models import Entity


class EntityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = [
            "name",
            "description",
            "plural",
            "documentation",
            "is_person",
        ]
