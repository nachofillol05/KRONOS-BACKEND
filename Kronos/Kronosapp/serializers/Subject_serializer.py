from rest_framework import serializers
from ..models import Subject
from .course_serializer import serializers

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'weeklyHours', 'color', 'abbreviation', 'school']