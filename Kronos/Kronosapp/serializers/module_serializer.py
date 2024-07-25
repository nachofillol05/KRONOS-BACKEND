from rest_framework import serializers
from  .year_serializer import YearSerializer
from ..models import Module

class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = ['id','name','description', 'year']