from Kronosapp.models import CustomUser
from Kronosapp.management.commands.seed_images import defaultuser

def seed_CustomUser_JM():
    # Preceptores
    preceptor_1ro = CustomUser.objects.create_user(
        email='preceptor1ro@secundaria.edu',
        password='password',
        first_name='Andrea',
        last_name='Quiroga',
        gender='femenino',
        document='26789022',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701200',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_preceptor_1ro,
        email_verified=True
    )

    preceptor_2do = CustomUser.objects.create_user(
        email='preceptor2do@secundaria.edu',
        password='password',
        first_name='Miguel',
        last_name='Bustamante',
        gender='masculino',
        document='27290123',
        profile_picture=defaultuser,
        hoursToWork=25,
        phone='3516701211',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_preceptor_2do,
        email_verified=True
    )
    preceptor_3ro = CustomUser.objects.create_user(
        email='preceptor3ro@secundaria.edu',
        password='password',
        first_name='Lucía',
        last_name='Fernández',
        gender='femenino',
        document='28901334',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701222',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_preceptor_3ro,
        email_verified=True
    )
    preceptor_4to = CustomUser.objects.create_user(
        email='preceptor4to@secundaria.edu',
        password='password',
        first_name='José',
        last_name='Morales',
        gender='masculino',
        document='29012445',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701233',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_preceptor_4to,
        email_verified=True
    )
    preceptor_5to = CustomUser.objects.create_user(
        email='preceptor5to@secundaria.edu',
        password='password',
        first_name='Elena',
        last_name='Ramírez',
        gender='femenino',
        document='30153456',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701244',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_preceptor_5to,
        email_verified=True
    )
    preceptor_6to = CustomUser.objects.create_user(
        email='preceptor6to@secundaria.edu',
        password='password',
        first_name='Ricardo',
        last_name='Guzmán',
        gender='masculino',
        document='32234567',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701255',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_preceptor_6to,
        email_verified=True
    )


    # Crear usuarios personalizados para la escuela "Jesús María"

    teacherJM = []

    # Directivo
    directive_user = CustomUser.objects.create_user(
        email='directive@secundaria.edu',
        password='password',
        first_name='marcelo',
        last_name='jimenez',
        gender='femenino',
        document='12345678',
        profile_picture=defaultuser,
        hoursToWork=25,
        phone='351410231',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_directive,
        email_verified=True
    )

    # Creación de profesores para cada materia
    teacher_matematica = CustomUser.objects.create_user(
        email='matematica@secundaria.edu',
        password='password',
        first_name='Juan',
        last_name='Rodríguez',
        gender='masculino',
        document='12365678',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701124',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_matematica,
        email_verified=True
    )
    teacherJM.append(teacher_matematica)  # Agregar profesor a la lista

    teacher_fisica = CustomUser.objects.create_user(
        email='fisica@secundaria.edu',
        password='password',
        first_name='Sofía',
        last_name='López',
        gender='femenino',
        document='23456789',
        profile_picture=defaultuser,
        hoursToWork=22,
        phone='3516701125',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_fisica,
        email_verified=True
    )
    teacherJM.append(teacher_fisica)

    teacher_quimica = CustomUser.objects.create_user(
        email='quimica@secundaria.edu',
        password='password',
        first_name='Martín',
        last_name='Pérez',
        gender='masculino',
        document='34567890',
        profile_picture=defaultuser,
        hoursToWork=25,
        phone='3516701126',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_quimica,
        email_verified=True
    )
    teacherJM.append(teacher_quimica)

    teacher_biologia = CustomUser.objects.create_user(
        email='biologia@secundaria.edu',
        password='password',
        first_name='Laura',
        last_name='García',
        gender='femenino',
        document='45678901',
        profile_picture=defaultuser,
        hoursToWork=24,
        phone='3516701127',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_biologia,
        email_verified=True
    )
    teacherJM.append(teacher_biologia)

    teacher_ingles = CustomUser.objects.create_user(
        email='ingles@secundaria.edu',
        password='password',
        first_name='Daniel',
        last_name='Suárez',
        gender='masculino',
        document='56784012',
        profile_picture=defaultuser,
        hoursToWork=18,
        phone='3516701128',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_ingles,
        email_verified=True
    )
    teacherJM.append(teacher_ingles)

    teacher_educacion_fisica = CustomUser.objects.create_user(
        email='educacionfisica@secundaria.edu',
        password='password',
        first_name='Lucía',
        last_name='Méndez',
        gender='femenino',
        document='67830123',
        profile_picture=defaultuser,
        hoursToWork=30,
        phone='3516701129',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_educacion_fisica,
        email_verified=True
    )
    teacherJM.append(teacher_educacion_fisica)

    teacher_religion = CustomUser.objects.create_user(
        email='religion@secundaria.edu',
        password='password',
        first_name='José',
        last_name='Aguilar',
        gender='masculino',
        document='78301234',
        profile_picture=defaultuser,
        hoursToWork=15,
        phone='3516701130',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_religion,
        email_verified=True
    )
    teacherJM.append(teacher_religion)

    teacher_latin = CustomUser.objects.create_user(
        email='latin@secundaria.edu',
        password='password',
        first_name='Marta',
        last_name='Vázquez',
        gender='femenino',
        document='89015345',
        profile_picture=defaultuser,
        hoursToWork=20,
        phone='3516701131',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_latin,
        email_verified=True
    )
    teacherJM.append(teacher_latin)

    teacher_geografia = CustomUser.objects.create_user(
        email='geografia@secundaria.edu',
        password='password',
        first_name='Ramiro',
        last_name='Romero',
        gender='masculino',
        document='90210456',
        profile_picture=defaultuser,
        hoursToWork=23,
        phone='3516701132',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_geografia,
        email_verified=True
    )
    teacherJM.append(teacher_geografia)

    teacher_lengua = CustomUser.objects.create_user(
        email='lengua2@secundaria.edu',
        password='password',
        first_name='Clara',
        last_name='Fernández',
        gender='femenino',
        document='15447893',
        profile_picture=defaultuser,
        hoursToWork=25,
        phone='3516701133',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_lengua,
        email_verified=True
    )
    teacherJM.append(teacher_lengua)

    teacher_informatica = CustomUser.objects.create_user(
        email='informatica@secundaria.edu',
        password='password',
        first_name='Luciano',
        last_name='Pereyra',
        gender='masculino',
        document='17894553',
        profile_picture=defaultuser,
        hoursToWork=30,
        phone='3516752234',
        documentType=dni,
        nationality=argentina,
        contactInfo=contact_info_informatica,
        email_verified=True
    )
    teacherJM.append(teacher_informatica)


"""
# Asignar directivos a la escuela
school.directives.add(directive_user)


year1.preceptors.add(preceptor_1ro)
year2.preceptors.add(preceptor_2do)
year3.preceptors.add(preceptor_3ro)
year4.preceptors.add(preceptor_4to)
year5.preceptors.add(preceptor_5to)
year6.preceptors.add(preceptor_6to)


    # Now handle the many-to-many relationships
    event_roles = [
        (event1, [teacher_role], [teacher_matematica, teacher_fisica]),
        (event2, [teacher_role], [teacher_quimica, teacher_biologia]),
        (event3, [teacher_role], [teacher_ingles, teacher_geografia]),
        (event4, [directive_role], [teacher_informatica]),
        (event5, [directive_role, teacher_role], [teacher_informatica, teacher_matematica, teacher_geografia]),
        (event6, [teacher_role], [teacher_quimica, teacher_ingles]),
        (event7, [directive_role, preceptor_role], [teacher_matematica, teacher_biologia]),
        (event8, [directive_role, teacher_role, preceptor_role], [teacher_educacion_fisica, teacher_lengua]),
        (event9, [teacher_role], [teacher_geografia, teacher_latin]),
        (event10, [directive_role, teacher_role], [teacher_religion, teacher_informatica]),
        (event11, [preceptor_role], [teacher_biologia, teacher_quimica, teacher_matematica]),
        (event12, [teacher_role], [teacher_educacion_fisica, teacher_religion]),
        (event13, [teacher_role, preceptor_role], [teacher_geografia, teacher_lengua, teacher_informatica]),
        (event14, [teacher_role], [teacher_fisica, teacher_matematica])
    ]

    # Add roles and affiliated teachers
    for event, roles, teachers in event_roles:
        event.roles.add(*roles)
        event.affiliated_teachers.add(*teachers)
"""