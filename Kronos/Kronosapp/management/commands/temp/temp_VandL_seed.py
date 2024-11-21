from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, AvailabilityState, EventType, Role, Action,
    
    ContactInformation, School, CustomUser, Module, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Event, CourseSubjects
)

import uuid
from django.utils import timezone
from datetime import time, timedelta, datetime
from .seed_images import *
class Command(BaseCommand):
    help = 'Seed database with initial data'
    # python manage.py seed
    def handle(self, *args, **options):#Seed Villada
        # Información de contacto para Villada
        contact_info_directive_villada = ContactInformation.objects.create(
            postalCode='4003',
            street='Avenida Belgrano',
            streetNumber='100',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_1ro_villada = ContactInformation.objects.create(
            postalCode='4003',
            street='Calle Salta',
            streetNumber='200',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_2do_villada = ContactInformation.objects.create(
            postalCode='4003',
            street='Calle Jujuy',
            streetNumber='300',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_3ro_villada = ContactInformation.objects.create(
            postalCode='4003',
            street='Calle Chacabuco',
            streetNumber='400',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        # Información de contacto para Lasalle
        contact_info_directive_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Lorenzo',
            streetNumber='500',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_1ro_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Juan',
            streetNumber='600',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_2do_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Entre Ríos',
            streetNumber='700',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_3ro_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Mendoza',
            streetNumber='800',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

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

        # Información de contacto para la escuela Villada
        contact_info_villada = ContactInformation.objects.create(
            postalCode='4003',
            street='Avenida Belgrano',
            streetNumber='100',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        # Información de contacto para la escuela Lasalle
        contact_info_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Lorenzo',
            streetNumber='500',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        # Crear escuela Villada
        school_villada = School.objects.create(
            name='Villada',
            abbreviation='VIL',
            logo=defaultuser,  # Define este logotipo en seed_images.py
            email='contacto@villada.edu',
            contactInfo=contact_info_villada
        )

        school_villada.directives.add(directive_villada)

        # Crear escuela Lasalle
        school_lasalle = School.objects.create(
            name='Lasalle',
            abbreviation='LAS',
            logo=defaultuser,  # Define este logotipo en seed_images.py
            email='contacto@lasalle.edu',
            contactInfo=contact_info_lasalle
        )

        # Módulos Villada
        modules_villada = []
        for i, day in enumerate(days_of_week, start=1):
            for j in range(1, 6):
                module_villada = Module.objects.create(
                    moduleNumber=j,
                    day=day,
                    startTime=time(7 + j, 0),
                    endTime=time(8 + j, 0),
                    school=school_villada
                )
                modules_villada.append(module_villada)

        # Módulos Lasalle
        modules_lasalle = []
        for i, day in enumerate(days_of_week, start=1):
            for j in range(1, 6):
                module_lasalle = Module.objects.create(
                    moduleNumber=j,
                    day=day,
                    startTime=time(9 + j, 0),
                    endTime=time(10 + j, 0),
                    school=school_lasalle
                )
                modules_lasalle.append(module_lasalle)

        # Crear años para Villada
        year1_villada = Year.objects.create(name='1er Año', number='1', school=school_villada)
        year2_villada = Year.objects.create(name='2do Año', number='2', school=school_villada)
        year3_villada = Year.objects.create(name='3er Año', number='3', school=school_villada)
        year4_villada = Year.objects.create(name='4to Año', number='4', school=school_villada)
        year5_villada = Year.objects.create(name='5to Año', number='5', school=school_villada)
        year6_villada = Year.objects.create(name='6to Año', number='6', school=school_villada)

        # Crear años para Lasalle
        year1_lasalle = Year.objects.create(name='1er Año', number='1', school=school_lasalle)
        year2_lasalle = Year.objects.create(name='2do Año', number='2', school=school_lasalle)
        year3_lasalle = Year.objects.create(name='3er Año', number='3', school=school_lasalle)
        year4_lasalle = Year.objects.create(name='4to Año', number='4', school=school_lasalle)
        year5_lasalle = Year.objects.create(name='5to Año', number='5', school=school_lasalle)
        year6_lasalle = Year.objects.create(name='6to Año', number='6', school=school_lasalle)

        # Asignar preceptores a años en Villada
        year1_villada.preceptors.add(preceptor_1ro_villada)
        year2_villada.preceptors.add(preceptor_2do_villada)

        # Asignar preceptores a años en Lasalle
        year1_lasalle.preceptors.add(preceptor_1ro_lasalle)
        year2_lasalle.preceptors.add(preceptor_2do_lasalle)

        # Crear cursos para Villada
        course_names = ['A', 'B', 'C']
        courses_villada = []
        for year in [year1_villada, year2_villada, year3_villada, year4_villada, year5_villada, year6_villada]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                courses_villada.append(course)

        # Crear cursos para Lasalle
        courses_lasalle = []
        for year in [year1_lasalle, year2_lasalle, year3_lasalle, year4_lasalle, year5_lasalle, year6_lasalle]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                courses_lasalle.append(course)

        # Materias para Villada
        subjects_villada = []
        subject_math_villada = Subject.objects.create(
            name="Matemáticas",
            color='#C0392B',  
            abbreviation="MAT",
            school=school_villada
        )
        subjects_villada.append(subject_math_villada)

        subject_physics_villada = Subject.objects.create(
            name="Física",
            color='#2980B9',  
            abbreviation="FIS",
            school=school_villada
        )
        subjects_villada.append(subject_physics_villada)

        # Materias para Lasalle
        subjects_lasalle = []
        subject_math_lasalle = Subject.objects.create(
            name="Matemáticas",
            color='#C0392B',  
            abbreviation="MAT",
            school=school_lasalle
        )
        subjects_lasalle.append(subject_math_lasalle)

        subject_physics_lasalle = Subject.objects.create(
            name="Física",
            color='#2980B9',  
            abbreviation="FIS",
            school=school_lasalle
        )
        subjects_lasalle.append(subject_physics_lasalle)

        # Asignar materias a cursos en Villada
        coursesubjects_villada = []
        for subject in subjects_villada:
            for course in courses_villada:
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(
                    studyPlan=studyPlan, 
                    subject=subject, 
                    course=course, 
                    weeklyHours=5
                )
                coursesubjects_villada.append(coursesubject)

        # Asignar materias a cursos en Lasalle
        coursesubjects_lasalle = []
        for subject in subjects_lasalle:
            for course in courses_lasalle:
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(
                    studyPlan=studyPlan, 
                    subject=subject, 
                    course=course, 
                    weeklyHours=5
                )
                coursesubjects_lasalle.append(coursesubject)

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

        # Asignar profesor a materia en Villada
        TeacherSubjectSchool.objects.create(
            school=school_villada,
            coursesubjects=coursesubjects_villada[0],  # Primer curso de Matemáticas
            teacher=teacher_math_villada
        )

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

        # Asignar profesor a materia en Lasalle
        TeacherSubjectSchool.objects.create(
            school=school_lasalle,
            coursesubjects=coursesubjects_lasalle[1],  # Primer curso de Física
            teacher=teacher_physics_lasalle
        )

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


        for module in modules_villada:
            TeacherAvailability.objects.create(
                module=module,
                teacher=teacher_math_villada,
                loadDate=datetime.now(),
                availabilityState=available
            )

        # Disponibilidad de profesores en Lasalle
        for module in modules_lasalle:
            TeacherAvailability.objects.create(
                module=module,
                teacher=teacher_physics_lasalle,
                loadDate=datetime.now(),
                availabilityState=not_available if module.moduleNumber % 2 == 0 else available
            )

        self.stdout.write(self.style.SUCCESS('\nDatabase successfully seeded!\n'))