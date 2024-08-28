from rest_framework import serializers
from ..models import CustomUser, TeacherSubjectSchool


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
