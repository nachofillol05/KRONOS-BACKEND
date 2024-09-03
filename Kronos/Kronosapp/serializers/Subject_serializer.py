# serializers.py
from rest_framework import serializers
from ..models import CourseSubjects, Subject, TeacherSubjectSchool


class TeacherSubjectSchoolSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name')

    class Meta:
        model = TeacherSubjectSchool
        fields = ['id', 'teacher_name']

class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='course.name')
    description = serializers.CharField(source='course.description')
    year = serializers.CharField(source='course.year')
    teacher_subject_schools = TeacherSubjectSchoolSerializer(source='teachersubjectschool_set', many=True)

    class Meta:
        model = CourseSubjects
        fields = ['id', 'name', 'description', 'year', 'studyPlan', 'teacher_subject_schools']

class SubjectWithCoursesSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(source='coursesubjects_set', many=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'color', 'abbreviation', 'courses']

