# serializers.py
from rest_framework import serializers
from ..models import CourseSubjects, Subject, Course

class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='course.name')
    description = serializers.CharField(source='course.description')
    year = serializers.CharField(source='course.year')

    class Meta:
        model = CourseSubjects
        fields = ['id', 'name', 'description', 'year', 'studyPlan']

class SubjectWithCoursesSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(source='coursesubjects_set', many=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'color', 'abbreviation', 'courses']
