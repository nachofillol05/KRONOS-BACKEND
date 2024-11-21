from Kronosapp.models import TeacherAvailability

# Crear disponibilidad de profesor en Jesús María
for j, teacher in enumerate(teacherJM):
    for i, module in enumerate(modulesJM):
        availabilityState = available if i % 3 < 2 else not_available
        TeacherAvailability.objects.create(
            module=module,
            teacher=teacher,
            loadDate=datetime.now(),
            availabilityState=availabilityState
        )