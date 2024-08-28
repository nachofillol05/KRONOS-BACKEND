from rest_framework import serializers
from ..models import CustomUser, ContactInformation, DocumentType, Nationality, TeacherSubjectSchool
from ..utils import convert_binary_to_image, convert_image_to_binary

class ContactInforSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class TeacherSubjectSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubjectSchool
        fields = ['Teacher', 'School']


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    contactInfo = ContactInforSerializer()
    documentType = DocumentTypeSerializer()
    nationality = NationalitySerializer()
    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj):
        imagen_binaria = obj.profile_picture

        if imagen_binaria:
            return convert_binary_to_image(imagen_binaria)
        return None

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
            'contactInfo',
            'dark_mode',
            'color',
            'phone',
            'profile_picture'
        ]
        
    

class UpdateUserSerializer(serializers.ModelSerializer):
    contactInfo = ContactInforSerializer()
    profile_picture = serializers.ImageField()

    class Meta:
        model = CustomUser
        read_only_fields = ['email']
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'document',
            'documentType',
            'nationality',
            'contactInfo',
            'dark_mode',
            'color',
            'phone',
            'profile_picture'
        ]

    
    def update(self, instance, validated_data):
        contact_info_data = validated_data.pop('contactInfo', None)
        if contact_info_data:
            contact_info_instance = instance.contactInfo
            for key, value in contact_info_data.items():
                setattr(contact_info_instance, key, value)
            contact_info_instance.save()

        imagen = validated_data.pop('profile_picture', None)
        if imagen:
            instance.profile_picture = convert_image_to_binary(imagen)

        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.profile_picture:
            representation['profile_picture'] = convert_binary_to_image(instance.profile_picture)
        else:
            representation['profile_picture'] = None
        return representation
