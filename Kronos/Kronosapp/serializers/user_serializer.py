from rest_framework import serializers
from ..models import CustomUser, ContactInformation, DocumentType, Nationality, TeacherSubjectSchool


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
class RegisterTeacherSubjectSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSubjectSchool
        fields = ['teacher', 'school']

    def create(self, validated_data):
        teacherschool = TeacherSubjectSchool.objects.create(**validated_data)
        teacherschool.save()
        return teacherschool


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    
    class Meta:
        model = CustomUser
        fields = [
            'pk',
            'email',
            'password',
            'first_name',
            'last_name',
            'documentType',
            'document',
            'phone'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True, 'write_only': True, 'min_length': 8},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'documentType': {'required': True},
            'document': {'required': True},
            'phone': {'required': True},
        }

    def validate_password(self, value):
        # faltan validaciones
        if len(value) < 8:
            raise serializers.ValidationError("Password must be greater than 8 characters.")
        return value
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value
    def validate_document(self, value):
        if CustomUser.objects.filter(document=value).exists():
            raise serializers.ValidationError("This document is already registed")
        return value
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save() 
        return user


class UserSerializer(serializers.ModelSerializer):
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
            'nationality',
            'contactInfo',
            'dark_mode',
            'color',
            'phone',
            'profile_picture'
        ]
        
    

class UpdateUserSerializer(serializers.ModelSerializer):
    contactInfo = ContactInforSerializer()

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
            # Actualizar la información de contacto manualmente
            contact_info_instance = instance.contactInfo
            for key, value in contact_info_data.items():
                setattr(contact_info_instance, key, value)
            contact_info_instance.save()

        return super().update(instance, validated_data)   
