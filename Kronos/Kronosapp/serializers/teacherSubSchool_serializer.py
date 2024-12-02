from rest_framework import serializers
from ..models import TeacherSubjectSchool, School, CustomUser

class TeacherSubjectSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubjectSchool
        fields = ['teacher', 'school', 'coursesubjects']
