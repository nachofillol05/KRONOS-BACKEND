# serializers.py
from rest_framework import serializers
from ..models import CourseSubjects, Subject, TeacherSubjectSchool, School

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id']


class TeacherSubjectSchoolSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name')
    teacher_id = serializers.IntegerField(source='teacher.id') 

    class Meta:
        model = TeacherSubjectSchool
        fields = ['id', 'teacher_name','teacher_id']

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

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['pk', 'name', 'abbreviation', 'color']

    def create(self, validated_data):
        school = validated_data.pop('school', None)
        subject = Subject.objects.create(school=school, **validated_data)
        return subject