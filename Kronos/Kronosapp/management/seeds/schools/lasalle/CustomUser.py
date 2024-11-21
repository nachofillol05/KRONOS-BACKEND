directive_lasalle = CustomUser.objects.create_user(
    email='directive@lasalle.edu',
    password='password',
    first_name='María',
    last_name='Gómez',
    gender='femenino',
    document='87651234',
    profile_picture=defaultuser,
    hoursToWork=30,
    phone='3816005678',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_directive_lasalle,
    email_verified=True
)

 # Preceptores Lasalle
preceptor_1ro_lasalle = CustomUser.objects.create_user(
    email='preceptor1ro@lasalle.edu',
    password='password',
    first_name='Cecilia',
    last_name='Moreno',
    gender='femenino',
    document='22345001',
    profile_picture=defaultuser,
    hoursToWork=20,
    phone='3816101234',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_preceptor_1ro_lasalle,
    email_verified=True
)

preceptor_2do_lasalle = CustomUser.objects.create_user(
    email='preceptor2do@lasalle.edu',
    password='password',
    first_name='Ricardo',
    last_name='Paz',
    gender='masculino',
    document='22345002',
    profile_picture=defaultuser,
    hoursToWork=25,
    phone='3816105678',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_preceptor_2do_lasalle,
    email_verified=True
)

teacherLS = []
# Profesores de Lasalle
teacher_physics_lasalle = CustomUser.objects.create_user(
    email='physics@lasalle.edu',
    password='password',
    first_name='Juan',
    last_name='Pérez',
    gender='masculino',
    document='67890123',
    profile_picture=defaultuser,
    hoursToWork=25,
    phone='3816701134',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_lasalle,
    email_verified=True
)
teacherLS.append(teacher_physics_lasalle)