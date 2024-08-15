from rest_framework import serializers
from ..models import Subject, CourseSubjects, Course


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'weeklyHours', 'color', 'abbreviation']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'year']


class CourseSubjectsSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    course = CourseSerializer()
    class Meta:
        model = CourseSubjects
        fields = ['id', 'subject', 'studyPlan', 'course']

