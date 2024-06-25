from rest_framework import serializers
from ..models import Year

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['id','name', 'description', 'number']
