from rest_framework import serializers
from .school_serializer import ModuleSerializer
from ..models import TeacherAvailability, CustomUser, Module, AvailabilityState

class AvailabilityStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityState
        fields = '__all__'

class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(required=True, queryset=CustomUser.objects.all())
    module_id = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        source='module',
        write_only=True
    )
    module = ModuleSerializer(read_only=True)
    availabilityState_id = serializers.PrimaryKeyRelatedField(
        queryset=AvailabilityState.objects.all(),
        source='availabilityState',
        write_only=True,
        required=True
    )
    availabilityState = AvailabilityStateSerializer(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'school'):
            self.fields['module'].queryset = Module.objects.filter(school=request.school)

    class Meta:
        model = TeacherAvailability
        fields = ['pk', 'module', 'module_id', 'loadDate', 'availabilityState', 'availabilityState_id', 'teacher']
        depth = 1
        extra_kwargs = {
            'loadDate': {'read_only': True},
            'availabilityState': {'required': True},
        }

    def validate(self, data):
        teacher = data.get('teacher')
        module = data.get('module')

        # Corregido: Excluir el registro actual en la validación de duplicados
        instance_id = self.instance.pk if self.instance else None
        if TeacherAvailability.objects.filter(teacher=teacher, module=module).exclude(pk=instance_id).exists():
            raise serializers.ValidationError({"module_id": "El módulo ya está en uso por el usuario."})
        return data
