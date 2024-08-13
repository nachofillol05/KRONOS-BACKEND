from rest_framework import serializers
from  .year_serializer import YearSerializer
from ..models import Course, Year

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['id','name', 'description', 'number']

class CourseSerializer(serializers.ModelSerializer):
    year = YearSerializer(many=False)

    class Meta:
        model = Course
        fields = ['id','name','description', 'year']