# Eventos para Lasalle
event_lasalle_1 = Event.objects.create(
    name='Capacitación docente en tecnología',
    startDate=timezone.now(),
    endDate=timezone.now() + timedelta(hours=4),
    school=school_lasalle,
    eventType=event_type_meeting
)
event_lasalle_1.roles.add(role_directive, role_teacher)
event_lasalle_1.affiliated_teachers.add(teacher_physics_lasalle)

event_lasalle_2 = Event.objects.create(
    name='Mantenimiento de la biblioteca',
    startDate=timezone.now() + timedelta(days=3),
    endDate=timezone.now() + timedelta(days=3, hours=5),
    school=school_lasalle,
    eventType=event_type_maintenance
)
event_lasalle_2.roles.add(role_directive)