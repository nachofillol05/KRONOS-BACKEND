from rest_framework import serializers
from ..models import Subject, Course

class courseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'year']

class SubjectSerializer(serializers.ModelSerializer):
    course = courseSerializer()
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'weeklyHours', 'color', 'abbreviation','course']