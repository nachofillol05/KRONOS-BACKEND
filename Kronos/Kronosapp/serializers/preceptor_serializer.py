from rest_framework import serializers
from ..models import Year
from .user_serializer import UserSerializer, CustomUser, ContactInforSerializer, NationalitySerializer, DocumentTypeSerializer


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year    
        fields = '__all__'


class PreceptorSerializer(UserSerializer):
    years = serializers.SerializerMethodField()
    contactInfo = ContactInforSerializer()
    documentType = DocumentTypeSerializer()
    nationality = NationalitySerializer()

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
            'years'
            'nationality',
            'dark_mode',
            'color',
            'contactInfo',
        ]


    def get_years(self, obj):
        # Obtiene los años asociados al preceptor
        preceptor_years = PreceptorYearSchool.objects.filter(preceptor=obj)
        years = preceptor_years.values_list('year', flat=True)
        return YearSerializer(Year.objects.filter(id__in=years), many=True).data
