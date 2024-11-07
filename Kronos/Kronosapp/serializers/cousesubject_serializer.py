from rest_framework import serializers
from ..models import CourseSubjects


class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubjects
        fields = ['studyPlan', 'subject', 'course', 'weeklyHours']
        
class CourseSubjectSerializerDetail(serializers.ModelSerializer):
    # Este serializer es solo para el detail, update, delete
    class Meta:
        model = CourseSubjects
        fields = ['studyPlan', 'subject', 'course', 'weeklyHours']
        extra_kwargs = {
            'subject': {'read_only': True},
            'course': {'read_only': True},
        }