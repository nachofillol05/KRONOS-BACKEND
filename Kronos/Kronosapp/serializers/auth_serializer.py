from rest_framework import serializers
from ..models import CustomUser, TeacherSubjectSchool, DocumentType


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
        document_type = int(self.initial_data.get('documentType'))
        
        if CustomUser.objects.filter(document=value).exists():
            raise serializers.ValidationError("This document is already registered.")

        try:
            dni = DocumentType.objects.get(name='DNI').id
            pasaporte = DocumentType.objects.get(name='Pasaporte').id
            cuit = DocumentType.objects.get(name='CUIT').id
        except DocumentType.DoesNotExist:
            raise serializers.ValidationError("El tipo de documento no es válido.")
        
        if document_type == dni:
            if len(value) < 8:
                raise serializers.ValidationError("El DNI debe tener al menos 8 caracteres.")
            if not value.isdigit():
                raise serializers.ValidationError("El DNI solo puede tener caracteres numericos.")
        elif document_type == pasaporte:
            if len(value) < 6 or len(value) > 9:
                raise serializers.ValidationError("El pasaporte debe tener entre 6 y 9 caracteres.")
            if not value.isalnum():
                raise serializers.ValidationError("El pasaporte no debe tener caracteres especiales.")
        elif document_type == cuit:
            if len(value) != 11:
                raise serializers.ValidationError("El CUIT debe tener 11 caracteres.")
            if not value.isdigit():
                raise serializers.ValidationError("El CUIT solo puede tener caracteres numericos.")
        else:
            raise serializers.ValidationError(f"Invalid document type {document_type}." )

        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save() 
        return user
