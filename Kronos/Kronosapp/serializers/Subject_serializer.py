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
    idCourse = serializers.IntegerField(source='course.id')
    name = serializers.CharField(source='course.name')
    description = serializers.CharField(source='course.description')
    year = serializers.CharField(source='course.year')
    teacher_subject_schools = TeacherSubjectSchoolSerializer(source='teachersubjectschool_set', many=True)

    class Meta:
        model = CourseSubjects
        fields = ['id', 'name', 'description', 'year', 'weeklyHours', 'studyPlan', 'teacher_subject_schools','idCourse', ]

class SubjectWithCoursesSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'color', 'abbreviation', 'courses']

    def get_courses(self, obj):
        teacher = self.context.get('teacher')
        courses = obj.coursesubjects_set.all()

        if teacher:
            courses = courses.filter(teachersubjectschool__teacher__id=teacher)
        
        serializer = CourseSerializer(courses, many=True, context=self.context)
        return serializer.data

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['pk', 'name', 'abbreviation', 'color']

    def create(self, validated_data):
        school = validated_data.pop('school', None)
        subject = Subject.objects.create(school=school, **validated_data)
        return subject