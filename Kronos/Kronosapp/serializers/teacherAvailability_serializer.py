from rest_framework import serializers
from ..models import TeacherAvailability

class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAvailability
        fields = '__all__'