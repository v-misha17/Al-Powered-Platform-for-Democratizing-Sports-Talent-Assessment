from rest_framework import serializers
from .models import AssessmentResult

class AssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResult
        fields = "__all__"
