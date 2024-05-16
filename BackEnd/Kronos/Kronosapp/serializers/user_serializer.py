from rest_framework import serializers
from ..models import CustomUser, ContactInformation


class ContactInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__' 


class UserSerializer(serializers.ModelSerializer):
    contactInfo = ContactInforSerializer()

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'gender',
            'document',
            'documentType',
            'nationality',
            'contactInfo',
            'dark_mode',
            'color1',
            'color2',
            'color3'
        ]
    
    def update(self, instance, validated_data):
        contact_info_data = validated_data.pop('contactInfo', None)
        if contact_info_data:
            # Actualizar la información de contacto manualmente
            contact_info_instance = instance.contactInfo
            for key, value in contact_info_data.items():
                setattr(contact_info_instance, key, value)
            contact_info_instance.save()

        return super().update(instance, validated_data)     
