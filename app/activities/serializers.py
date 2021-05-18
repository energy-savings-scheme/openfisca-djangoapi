
from rest_framework import serializers
from activities.models import Activity


class ActivityListSerializer(serializers.ModelSerializer):
    implementation = serializers.StringRelatedField(many=True)
    equipment = serializers.StringRelatedField(many=True)
    eligibility = serializers.StringRelatedField(many=True)
    energy_savings = serializers.StringRelatedField()

    class Meta:
        model = Activity
        fields = [
            "version_code",
            "version_name",
            "sub_method",
            "activity_name",
            "eligibility",
            "equipment",
            "implementation",
            "energy_savings"]
        depth = 0
