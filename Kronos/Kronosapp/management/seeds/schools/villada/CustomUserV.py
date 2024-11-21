# Directivos
directive_villada = CustomUser.objects.create_user(
    email='directive@villada.edu',
    password='password',
    first_name='Carlos',
    last_name='Luna',
    gender='masculino',
    document='87654321',
    profile_picture=defaultuser,
    hoursToWork=30,
    phone='3816001234',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_directive_villada,
    email_verified=True
)


# Preceptores Villada
preceptor_1ro_villada = CustomUser.objects.create_user(
    email='preceptor1ro@villada.edu',
    password='password',
    first_name='Ana',
    last_name='Torres',
    gender='femenino',
    document='12345001',
    profile_picture=defaultuser,
    hoursToWork=20,
    phone='3816006789',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_preceptor_1ro_villada,
    email_verified=True
)

preceptor_2do_villada = CustomUser.objects.create_user(
    email='preceptor2do@villada.edu',
    password='password',
    first_name='Luis',
    last_name='Sánchez',
    gender='masculino',
    document='12345002',
    profile_picture=defaultuser,
    hoursToWork=25,
    phone='3816007890',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_preceptor_2do_villada,
    email_verified=True
)

# Profesores de Villada
teacher_math_villada = CustomUser.objects.create_user(
    email='math@villada.edu',
    password='password',
    first_name='Pedro',
    last_name='Martínez',
    gender='masculino',
    document='56789012',
    profile_picture=defaultuser,
    hoursToWork=20,
    phone='3816701124',
    documentType=dni,
    nationality=argentina,
    contactInfo=contact_info_villada,
    email_verified=True
)
