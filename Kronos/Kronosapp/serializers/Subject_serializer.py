from rest_framework import serializers
from ..models import Subject
from .course_serializer import CourseSerializer

class SubjectSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'weeklyHours', 'color', 'abbreviation', 'school']