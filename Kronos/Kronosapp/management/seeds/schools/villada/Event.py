# Eventos para Villada
event_villada_1 = Event.objects.create(
    name='Reunión pedagógica',
    startDate=timezone.now(),
    endDate=timezone.now() + timedelta(hours=3),
    school=school_villada,
    eventType=event_type_meeting
)
event_villada_1.roles.add(role_directive, role_teacher)
event_villada_1.affiliated_teachers.add(teacher_math_villada)

event_villada_2 = Event.objects.create(
    name='Excursión al museo histórico',
    startDate=timezone.now() + timedelta(days=7),
    endDate=timezone.now() + timedelta(days=7, hours=6),
    school=school_villada,
    eventType=event_type_trip
)
event_villada_2.roles.add(role_teacher, role_preceptor)
event_villada_2.affiliated_teachers.add(teacher_math_villada)
