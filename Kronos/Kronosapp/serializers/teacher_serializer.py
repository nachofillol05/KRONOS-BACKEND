from rest_framework import serializers
from ..models import ContactInformation, CustomUser, DocumentType, Nationality, TeacherAvailability, TeacherSubjectSchool

class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = '__all__'

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['name', 'description']

class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ['name', 'description']

class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='availabilityState.name')
    class Meta:
        model = TeacherAvailability
        fields = ['module', 'loadDate', 'state']

class TeacherSubjectSchoolSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='coursesubjects.subject.name', allow_blank=True, default='')
    school_name = serializers.CharField(source='school.name')

    class Meta:
        model = TeacherSubjectSchool
        fields = ['subject_name', 'school_name']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.coursesubjects is None:
            representation['subject_name'] = ''
        elif instance.coursesubjects.subject.name is None:
            representation['subject_name'] = ''
        return representation
        
class TeacherSerializer(serializers.ModelSerializer):
    contactInfo = ContactInformationSerializer()
    documentType = DocumentTypeSerializer()
    nationality = NationalitySerializer()
    availability = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'gender', 'profile_picture', 'phone', 'email', 'document', 'documentType', 'nationality', 'email_verified', 'contactInfo', 'availability', 'subjects']

    def get_availability(self, obj):
        availabilities = obj.teacheravailability_set.all()
        return TeacherAvailabilitySerializer(availabilities, many=True).data

    def get_subjects(self, obj):
        subjects = obj.teachersubjectschool_set.all()
        return TeacherSubjectSchoolSerializer(subjects, many=True).data

class CreateTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'document', 'documentType', 'nationality', 'email_verified']

    def create(self, validated_data):
        contact_info_data = validated_data.pop('contactInfo', None)
        document_type_data = validated_data.pop('documentType', None)
        nationality_data = validated_data.pop('nationality', None)

        if contact_info_data:
            contact_info = ContactInformation.objects.create(**contact_info_data)
            validated_data['contactInfo'] = contact_info

        if document_type_data:
            document_type = DocumentType.objects.get_or_create(**document_type_data)[0]
            validated_data['documentType'] = document_type

        if nationality_data:
            nationality = Nationality.objects.get_or_create(**nationality_data)[0]
            validated_data['nationality'] = nationality

        teacher = CustomUser.objects.create(**validated_data)
        return teacher
