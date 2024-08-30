from rest_framework import serializers
from ..models import Nationality

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ['id', 'name', 'description']