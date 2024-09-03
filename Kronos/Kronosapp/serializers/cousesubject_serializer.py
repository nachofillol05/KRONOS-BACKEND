from rest_framework import serializers
from ..models import CourseSubjects



class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubjects
        fields = ['studyPlan', 'subject', 'course', 'weeklyHours']
        
