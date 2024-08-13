from rest_framework import serializers
from ..models import School, ContactInformation, CustomUser, Module


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'


class DirectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['pk','first_name', 'last_name', 'gender', 'email']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
    
    def to_representation(self, instance):
        instance.endTime = instance.endTime.replace(second=0, microsecond=0)
        return super().to_representation(instance)


class ReadSchoolSerializer(serializers.ModelSerializer):
    #contactInfo = ContactInformationSerializer()
    #directives = DirectiveSerializer(many=True)

    class Meta:
        model = School
        fields = ['pk', 'name', 'logo']
        # , 'abbreviation', 'logo', 'email', 'directives', 'contactInfo'
    
    def create(self, validated_data):
        directives_data = validated_data.pop('directives', [])

        school = School.objects.create(**validated_data)
        school.directives.set(directives_data)

        return school


class IdDirectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id'] 


class CreateSchoolSerializer(serializers.ModelSerializer):
    contactInfo = ContactInformationSerializer()

    class Meta:
        model = School
        fields = ['pk','name', 'abbreviation', 'logo', 'email', 'directives', 'contactInfo']

    def create(self, validated_data):
        contact_info_data = validated_data.pop('contactInfo')
        directives_data = validated_data.pop('directives', [])

        contact_info = ContactInformation.objects.create(**contact_info_data)
        school = School.objects.create(contactInfo=contact_info, **validated_data)

        school.directives.set(directives_data)
        return school

