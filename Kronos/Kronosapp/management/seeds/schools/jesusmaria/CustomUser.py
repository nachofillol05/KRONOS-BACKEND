from django.contrib.auth.hashers import make_password
import random
from Kronosapp.models import CustomUser,DocumentType,Nationality,ContactInformation, School, Year
from Kronosapp.management.commands.seed_images import defaultuser

def seed_CustomUser_JM():

    dni = DocumentType.objects.get(name='DNI')
    argentina = Nationality.objects.get(name='Argentina')
    contactInfo_list = ContactInformation.objects.all()

    # Defines all users to be created
    user_list = [
        # Directives
        {'email': 'directive@secundaria.edu', 'first_name': 'Marcelo', 'last_name': 'Jimenez', 'gender': 'femenino', 'document': '12345678', 'phone': '351410231', 'hoursToWork': 25},

        # Preceptors
        {'email': 'preceptor1ro@secundaria.edu', 'first_name': 'Andrea', 'last_name': 'Quiroga', 'gender': 'femenino', 'document': '26789022', 'phone': '3516701200', 'hoursToWork': 20},
        {'email': 'preceptor2do@secundaria.edu', 'first_name': 'Miguel', 'last_name': 'Bustamante', 'gender': 'masculino', 'document': '27290123', 'phone': '3516701211', 'hoursToWork': 25},
        {'email': 'preceptor3ro@secundaria.edu', 'first_name': 'Lucía', 'last_name': 'Fernández', 'gender': 'femenino', 'document': '28901334', 'phone': '3516701222', 'hoursToWork': 20},
        {'email': 'preceptor4to@secundaria.edu', 'first_name': 'José', 'last_name': 'Morales', 'gender': 'masculino', 'document': '29012445', 'phone': '3516701233', 'hoursToWork': 20},
        {'email': 'preceptor5to@secundaria.edu', 'first_name': 'Elena', 'last_name': 'Ramírez', 'gender': 'femenino', 'document': '30153456', 'phone': '3516701244', 'hoursToWork': 20},
        {'email': 'preceptor6to@secundaria.edu', 'first_name': 'Ricardo', 'last_name': 'Guzmán', 'gender': 'masculino', 'document': '32234567', 'phone': '3516701255', 'hoursToWork': 20},
        
        # Teachers
        {'email': 'matematica@secundaria.edu', 'first_name': 'Juan', 'last_name': 'Rodríguez', 'gender': 'masculino', 'document': '12365678', 'phone': '3516701124', 'hoursToWork': 20},
        {'email': 'fisica@secundaria.edu', 'first_name': 'Sofía', 'last_name': 'López', 'gender': 'femenino', 'document': '23456789', 'phone': '3516701125', 'hoursToWork': 22},
        {'email': 'quimica@secundaria.edu', 'first_name': 'Martín', 'last_name': 'Pérez', 'gender': 'masculino', 'document': '34567890', 'phone': '3516701126', 'hoursToWork': 25},
        {'email': 'biologia@secundaria.edu', 'first_name': 'Laura', 'last_name': 'García', 'gender': 'femenino', 'document': '45678901', 'phone': '3516701127', 'hoursToWork': 24},
        {'email': 'ingles@secundaria.edu', 'first_name': 'Daniel', 'last_name': 'Suárez', 'gender': 'masculino', 'document': '56784012', 'phone': '3516701128', 'hoursToWork': 18},
        {'email': 'educacionfisica@secundaria.edu', 'first_name': 'Lucía', 'last_name': 'Méndez', 'gender': 'femenino', 'document': '67830123', 'phone': '3516701129', 'hoursToWork': 30},
        {'email': 'religion@secundaria.edu', 'first_name': 'José', 'last_name': 'Aguilar', 'gender': 'masculino', 'document': '78301234', 'phone': '3516701130', 'hoursToWork': 15},
        {'email': 'latin@secundaria.edu', 'first_name': 'Marta', 'last_name': 'Vázquez', 'gender': 'femenino', 'document': '89015345', 'phone': '3516701131', 'hoursToWork': 20},
        {'email': 'geografia@secundaria.edu', 'first_name': 'Ramiro', 'last_name': 'Romero', 'gender': 'masculino', 'document': '90210456', 'phone': '3516701132', 'hoursToWork': 23},
        {'email': 'lengua2@secundaria.edu', 'first_name': 'Clara', 'last_name': 'Fernández', 'gender': 'femenino', 'document': '15447893', 'phone': '3516701133', 'hoursToWork': 25},
        {'email': 'informatica@secundaria.edu', 'first_name': 'Luciano', 'last_name': 'Pereyra', 'gender': 'masculino', 'document': '17894553', 'phone': '3516752234', 'hoursToWork': 30}
    ]

    # Bulk Creation of custom users
    CustomUser.objects.bulk_create(
        CustomUser(
            email=user['email'],
            password=make_password('password'),
            first_name=user['first_name'],
            last_name=user['last_name'],
            gender=user['gender'],
            document=user['document'],
            profile_picture=defaultuser,
            hoursToWork=user['hoursToWork'],
            phone=user['phone'],
            documentType=dni,
            nationality=argentina,
            contactInfo=contactInfo_list[i],
            email_verified=True
        )
        for i,user in enumerate(user_list)
    )

    
    school = School.objects.get(name='Jesus Maria')
    directive_user = CustomUser.objects.first()
    
    # Asignar directivos a la escuela
    school.directives.add(directive_user)

    year1 = Year.objects.get(id=1)
    year2 = Year.objects.get(id=1)
    year3 = Year.objects.get(id=1)
    year4 = Year.objects.get(id=1)
    year5 = Year.objects.get(id=1)
    year6 = Year.objects.get(id=1)

    year1.preceptors.add(preceptor_1ro)
    year2.preceptors.add(preceptor_2do)
    year3.preceptors.add(preceptor_3ro)
    year4.preceptors.add(preceptor_4to)
    year5.preceptors.add(preceptor_5to)
    year6.preceptors.add(preceptor_6to)

    """
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
