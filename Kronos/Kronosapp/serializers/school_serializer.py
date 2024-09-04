from rest_framework import serializers
from ..utils import convert_binary_to_image, convert_image_to_binary
from ..models import School, ContactInformation, CustomUser, Module
from .user_serializer import ContactInforSerializer


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


class ReadUserSchoolSerializer(serializers.ModelSerializer):
    contactInfo = ContactInformationSerializer()
    directives = DirectiveSerializer(many=True)

    class Meta:
        model = School
        fields = ['pk', 'name', 'logo' , 'abbreviation', 'logo', 'email', 'directives', 'contactInfo']
        
    
    def create(self, validated_data):
        directives_data = validated_data.pop('directives', [])

        school = School.objects.create(**validated_data)
        school.directives.set(directives_data)

        return school


class IdDirectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id']


class ReadSchoolSerializer(serializers.ModelSerializer):
    contactInfo = ContactInforSerializer()
    logo = serializers.ImageField(required=False)

    class Meta:
        model = School
        fields = ['pk', 'name', 'logo' , 'abbreviation', 'logo', 'email', 'directives', 'contactInfo']
        read_only_fields = ['email', 'directives']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.logo:
            representation['logo'] = convert_binary_to_image(instance.logo)
        else:
            representation['logo'] = None
        return representation
    
    def update(self, instance, validated_data):
        contact_info_data = validated_data.pop('contactInfo', None)
        if contact_info_data:
            contact_info_instance = instance.contactInfo
            for key, value in contact_info_data.items():
                setattr(contact_info_instance, key, value)
            contact_info_instance.save()
        imagen = validated_data.pop('logo', None)
        print(imagen)
        if imagen:
            instance.logo = convert_image_to_binary(imagen)

        return super().update(instance, validated_data)


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

