from rest_framework import serializers
from .module_serializer import ModuleSerializer
from ..models import Schedules, CustomUser, TeacherSubjectSchool, CourseSubjects, Action, Course, Subject

class SubjectSeriazlizer():
    class Meta:
        model = Subject
        fields = ['pk', 'name', 'color', 'abbreviation']

class CourseSeriazlizer():
    class Meta:
        model = Course
        fields = ['pk', 'name']

class CourseSubjectSeriazlizer():
    course = CourseSeriazlizer()
    subject = SubjectSeriazlizer()

    class Meta:
        model = CourseSubjects
        fields = '__all__'

class TeacherSerializer():
    class Meta:
        model = CustomUser
        fields = ['first_name', '']

class tssSerializer(serializers.ModelSerializer):
    coursesubjects = CourseSubjectSeriazlizer()

    class Meta:
        model = TeacherSubjectSchool
        fields = ['pk', 'coursesubjects', 'teacher']

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    tssId = tssSerializer()
    module = ModuleSerializer()
    action = ActionSerializer()

    class Meta:
        model = Schedules
        fields = '__all__'
