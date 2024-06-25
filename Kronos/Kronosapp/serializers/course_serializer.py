from rest_framework import serializers
from  .year_serializer import YearSerializer
from ..models import Course

class CourseSerializer(serializers.ModelSerializer):
    year = YearSerializer(many=False)

    class Meta:
        model = Course
        fields = ['id','name','description', 'year']