from rest_framework import serializers
from ..models import Schedules, CustomUser, TeacherSubjectSchool, CourseSubjects, Subject

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'profile_picture']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['pk', 'name', 'abbreviation', 'color']

class CoursesubjectsSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = CourseSubjects
        fields = ['pk', 'subject', 'course']



class TSSforscheduleSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    coursesubjects = CoursesubjectsSerializer()
    class Meta:
        model = TeacherSubjectSchool
        fields = ['pk', 'coursesubjects', 'teacher']

class ScheduleSerializer(serializers.ModelSerializer):
    tssId = TSSforscheduleSerializer()
    class Meta:
        model = Schedules
        fields = ['pk', 'module', 'tssId']

class CreateScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ['pk', 'module', 'tssId', 'action', 'date']