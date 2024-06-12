from rest_framework import serializers
from ..models import Year
from .user_serializer import UserSerializer, CustomUser, ContactInforSerializer


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year    
        fields = '__all__'


class PreceptorSerializer(UserSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'document',
            'documentType',
            'nationality',
            'dark_mode',
            'color',
            'contactInfo',
            'years'
        ]
