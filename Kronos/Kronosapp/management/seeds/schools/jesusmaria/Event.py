# Crear evento
event1 = Event.objects.create(
    name='Paro general de transporte',
    startDate=timezone.now(),
    endDate=timezone.now() + timedelta(days=1),
    school=school,
    eventType=event_type1
)
event1.roles.add(teacher_role)
event1.affiliated_teachers.add(teacher_matematica, teacher_fisica)

event2 = Event.objects.create(
    name='Excursión al museo de ciencias',
    startDate=timezone.now() + timedelta(days=1),
    endDate=timezone.now() + timedelta(days=0, hours=6),
    school=school,
    eventType=event_type2
)
event2.roles.add(teacher_role)
event2.affiliated_teachers.add(teacher_quimica, teacher_biologia)

event3 = Event.objects.create(
    name='Paro docente provincial',
    startDate=timezone.now() + timedelta(days=7),
    endDate=timezone.now() + timedelta(days=7, hours=10),
    school=school,
    eventType=event_type3
)
event3.roles.add(teacher_role)
event3.affiliated_teachers.add(teacher_ingles, teacher_geografia)

event4 = Event.objects.create(
    name='Taller docente de actualización pedagógica',
    startDate=timezone.now() + timedelta(days=10),
    endDate=timezone.now() + timedelta(days=10, hours=4),
    school=school,
    eventType=event_type4
)
event4.roles.add(directive_role)
event4.affiliated_teachers.add(teacher_informatica)

event5 = Event.objects.create(
    name='Fumigacion',
    startDate=timezone.now() + timedelta(days=7),
    endDate=timezone.now() + timedelta(days=7, hours=4),
    school=school,
    eventType=event_type
)
event5.roles.add(directive_role,teacher_role)
event5.affiliated_teachers.add(teacher_informatica, teacher_matematica,teacher_geografia)

event6 = Event.objects.create(
    name='Capacitación en tecnologías educativas',
    startDate=timezone.now()  + timedelta(days=15),
    endDate=timezone.now()  + timedelta(days=15, hours=8),
    school=school,
    eventType=event_type4
)
event6.roles.add(teacher_role)
event6.affiliated_teachers.add(teacher_quimica, teacher_ingles)

event7 = Event.objects.create(
    name='Día de puertas abiertas',
    startDate=timezone.now()    + timedelta(days=20),
    endDate=timezone.now()  + timedelta(days=20, hours=6),
    school=school,
    eventType=event_type2
)
event7.roles.add(directive_role, preceptor_role)
event7.affiliated_teachers.add(teacher_matematica, teacher_biologia)

event8 = Event.objects.create(
    name='Simulacro de evacuación',
    startDate=timezone.now()    + timedelta(days=3),
    endDate=timezone.now()   + timedelta(days=3, hours=1),
    school=school,
    eventType=event_type5
)
event8.roles.add(directive_role, teacher_role, preceptor_role)
event8.affiliated_teachers.add(teacher_educacion_fisica, teacher_lengua)

event9 = Event.objects.create(
    name='Charlas sobre educación ambiental',
    startDate=timezone.now()    + timedelta(days=5),
    endDate=timezone.now()    + timedelta(days=5, hours=3),
    school=school,
    eventType=event_type2
)
event9.roles.add(teacher_role)
event9.affiliated_teachers.add(teacher_geografia, teacher_latin)

event10 = Event.objects.create(
    name='Jornada de salud y bienestar',
    startDate=timezone.now()    + timedelta(days=12),
    endDate=timezone.now()    + timedelta(days=12, hours=4),
    school=school,
    eventType=event_type4
)
event10.roles.add(directive_role, teacher_role)
event10.affiliated_teachers.add(teacher_religion, teacher_informatica)

# Eventos que ocurren durante el mismo periodo para probar la concurrencia de eventos
event11 = Event.objects.create(
    name='Feria del libro escolar',
    startDate=timezone.now()    + timedelta(days=25),
    endDate=timezone.now()   + timedelta(days=26),
    school=school,
    eventType=event_type2
)
event11.roles.add(preceptor_role)
event11.affiliated_teachers.add(teacher_biologia, teacher_quimica, teacher_matematica)

event12 = Event.objects.create(
    name='Competencia deportiva interescolar',
    startDate=timezone.now()    + timedelta(days=26),
    endDate=timezone.now() + timedelta(days=27, hours=5),
    school=school,
    eventType=event_type
)
event12.roles.add(teacher_role)
event12.affiliated_teachers.add(teacher_educacion_fisica, teacher_religion)

# Evento a largo plazo que dure varios días
event13 = Event.objects.create(
    name='Semana de actividades culturales',
    startDate=timezone.now()    + timedelta(days=30),
    endDate=timezone.now()    + timedelta(days=34, hours=12),
    school=school,
    eventType=event_type2
)
event13.roles.add(teacher_role, preceptor_role)
event13.affiliated_teachers.add(teacher_geografia, teacher_lengua, teacher_informatica)

# Evento simultáneo con restricciones de roles
event14 = Event.objects.create(
    name='Capacitación en primeros auxilios',
    startDate=timezone.now()   + timedelta(days=10),
    endDate=timezone.now()    + timedelta(days=10, hours=3),
    school=school,
    eventType=event_type4
)
event14.roles.add(teacher_role)
event14.affiliated_teachers.add(teacher_fisica, teacher_matematica)
