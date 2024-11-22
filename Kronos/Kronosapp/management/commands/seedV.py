


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
    def handle(self, *args, **options):
        dni = DocumentType.objects.get(name="DNI")
        passport = DocumentType.objects.get(name="Pasaporte")
        cuit = DocumentType.objects.get(name="CUIT")

        # Crear nacionalidades
        argentina = Nationality.objects.get(name="Argentina", description="Nacionalidad argentina")
        uruguay = Nationality.objects.get(name="Uruguay", description="Nacionalidad uruguaya")
        brasil = Nationality.objects.get(name="Brasil", description="Nacionalidad brasileña")
        paraguay = Nationality.objects.get(name="Paraguay", description="Nacionalidad paraguaya")
        chile = Nationality.objects.get(name="Chile", description="Nacionalidad chilena")
        bolivia = Nationality.objects.get(name="Bolivia", description="Nacionalidad boliviana")
        peru = Nationality.objects.get(name="Perú", description="Nacionalidad peruana")
        otros = Nationality.objects.get(name="Otros", description="Nacionalidad otros")

        # estados de disponibilidad
        available = AvailabilityState.objects.get(name="Disponible", isEnabled=True)
        not_available = AvailabilityState.objects.get(name="No disponible", isEnabled=False)
        asigned = AvailabilityState.objects.get(name="Asignado", isEnabled=False)

        # tipos de eventos
        event_type1 = EventType.objects.get(name='Paro de transporte')
        event_type2 = EventType.objects.get(name='Viaje escolar')
        event_type3 = EventType.objects.get(name='Paro docente')
        event_type4 = EventType.objects.get(name='Taller Docente')
        event_type5 = EventType.objects.get(name='Mantenimiento Infraestructura')
        event_type = EventType.objects.get(name='Otro')

        # roles
        role_directive = Role.objects.get(name='Directivo')
        role_teacher = Role.objects.get(name='Profesor')
        role_preceptor = Role.objects.get(name='Preceptor')

        #contact information
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




        # Profesores
        contact_info_math_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Mitre',
            streetNumber='103',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_physics_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Mitre',
            streetNumber='104',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_chemistry_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Rivadavia',
            streetNumber='105',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_biology_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Rivadavia',
            streetNumber='106',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_english_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Buenos Aires',
            streetNumber='107',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_history_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Buenos Aires',
            streetNumber='108',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_geography_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Belgrano',
            streetNumber='109',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_literature_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Belgrano',
            streetNumber='110',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_computer_science_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Mendoza',
            streetNumber='111',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_art_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Mendoza',
            streetNumber='112',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_philosophy_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Salta',
            streetNumber='113',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_music_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Salta',
            streetNumber='114',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_physical_education_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Jujuy',
            streetNumber='115',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_religion_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Jujuy',
            streetNumber='116',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_electricity_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Entre Ríos',
            streetNumber='117',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_mechanics_villada = ContactInformation.objects.create(
            postalCode='4005',
            street='Calle Entre Ríos',
            streetNumber='118',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        #contact information escuela villada
        contact_info_villada = ContactInformation.objects.create(
            postalCode='4003',
            street='Avenida Belgrano',
            streetNumber='100',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        directives = []
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
        directives.append(directive_villada)


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

        teacherV = []
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
            contactInfo=contact_info_math_villada,
            email_verified=True
        )
        teacherV.append(teacher_math_villada)

        teacher_physics_villada = CustomUser.objects.create_user(
            email='physics@villada.edu',
            password='password',
            first_name='Roberto',
            last_name='Gómez',
            gender='masculino',
            document='56789013',
            profile_picture=defaultuser,
            hoursToWork=25,
            phone='3816701125',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_physics_villada,
            email_verified=True
        )
        teacherV.append(teacher_physics_villada)

        teacher_chemistry_villada = CustomUser.objects.create_user(
            email='chemistry@villada.edu',
            password='password',
            first_name='María',
            last_name='Rodríguez',
            gender='femenino',
            document='56789014',
            profile_picture=defaultuser,
            hoursToWork=24,
            phone='3816701126',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_chemistry_villada,
            email_verified=True
        )
        teacherV.append(teacher_chemistry_villada)

        teacher_biology_villada = CustomUser.objects.create_user(
            email='biology@villada.edu',
            password='password',
            first_name='Claudia',
            last_name='Fernández',
            gender='femenino',
            document='56789015',
            profile_picture=defaultuser,
            hoursToWork=26,
            phone='3816701127',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_biology_villada,
            email_verified=True
        )
        teacherV.append(teacher_biology_villada)

        teacher_english_villada = CustomUser.objects.create_user(
            email='english@villada.edu',
            password='password',
            first_name='Lucas',
            last_name='Pereyra',
            gender='masculino',
            document='56789016',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3816701128',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_english_villada,
            email_verified=True
        )
        teacherV.append(teacher_english_villada)

        teacher_history_villada = CustomUser.objects.create_user(
            email='history@villada.edu',
            password='password',
            first_name='Mónica',
            last_name='Suárez',
            gender='femenino',
            document='56789017',
            profile_picture=defaultuser,
            hoursToWork=27,
            phone='3816701129',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_history_villada,
            email_verified=True
        )
        teacherV.append(teacher_history_villada)

        teacher_geography_villada = CustomUser.objects.create_user(
            email='geography@villada.edu',
            password='password',
            first_name='Diego',
            last_name='Aguirre',
            gender='masculino',
            document='56789018',
            profile_picture=defaultuser,
            hoursToWork=26,
            phone='3816701130',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_geography_villada,
            email_verified=True
        )
        teacherV.append(teacher_geography_villada)

        teacher_literature_villada = CustomUser.objects.create_user(
            email='literature@villada.edu',
            password='password',
            first_name='Nora',
            last_name='Vega',
            gender='femenino',
            document='56789019',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3816701131',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_literature_villada,
            email_verified=True
        )
        teacherV.append(teacher_literature_villada)

        teacher_computer_science_villada = CustomUser.objects.create_user(
            email='computerscience@villada.edu',
            password='password',
            first_name='César',
            last_name='Alonso',
            gender='masculino',
            document='56789020',
            profile_picture=defaultuser,
            hoursToWork=25,
            phone='3816701132',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_computer_science_villada,
            email_verified=True
        )
        teacherV.append(teacher_computer_science_villada)

        teacher_art_villada = CustomUser.objects.create_user(
            email='art@villada.edu',
            password='password',
            first_name='Valeria',
            last_name='López',
            gender='femenino',
            document='56789021',
            profile_picture=defaultuser,
            hoursToWork=18,
            phone='3816701133',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_art_villada,
            email_verified=True
        )
        teacherV.append(teacher_art_villada)

        teacher_philosophy_villada = CustomUser.objects.create_user(
            email='philosophy@villada.edu',
            password='password',
            first_name='Alberto',
            last_name='Medina',
            gender='masculino',
            document='56789022',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3816701134',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_philosophy_villada,
            email_verified=True
        )
        teacherV.append(teacher_philosophy_villada)

        teacher_mechanics_villada = CustomUser.objects.create_user(
            email='mechanics@villada.edu',
            password='password',
            first_name='Federico',
            last_name='Giménez',
            gender='masculino',
            document='56789023',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3816701135',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_mechanics_villada, 
            email_verified=True
        )
        teacherV.append(teacher_mechanics_villada)

        teacher_electricity_villada = CustomUser.objects.create_user(
            email='electricity@villada.edu',
            password='password',
            first_name='Esteban',
            last_name='Ortiz',
            gender='masculino',
            document='56789024',
            profile_picture=defaultuser,
            hoursToWork=28,
            phone='3816701136',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_electricity_villada,  
            email_verified=True
        )
        teacherV.append(teacher_electricity_villada)



        # Crear escuela Villada
        school_villada = School.objects.create(
            name='Villada',
            abbreviation='VIL',
            logo=logoits,  # Define este logotipo en seed_images.py
            email='contacto@villada.edu',
            contactInfo=contact_info_villada
        )

        # Módulos Villada
        days_of_week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
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

        # Crear años para Villada
        year1_villada = Year.objects.create(name='1er Año', number='1', school=school_villada)
        year2_villada = Year.objects.create(name='2do Año', number='2', school=school_villada)
        year3_villada = Year.objects.create(name='3er Año', number='3', school=school_villada)
        year4_villada = Year.objects.create(name='4to Año', number='4', school=school_villada)
        year5_villada = Year.objects.create(name='5to Año', number='5', school=school_villada)
        year6_villada = Year.objects.create(name='6to Año', number='6', school=school_villada)
        year7_villada = Year.objects.create(name='7mo Año', number='7', school=school_villada)

        # Crear cursos para Villada
        course_names = ['A', 'B', 'C']
        courses_villada = []
        for year in [year1_villada, year2_villada, year3_villada, year4_villada, year5_villada, year6_villada, year7_villada]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                courses_villada.append(course)

        # Crear materias para Villada
        subjectsV = []
        subject_math_villada = Subject.objects.create(
            name="Matemáticas",
            color='#C0392B',  
            abbreviation="MAT",
            school=school_villada
        )
        subjectsV.append(subject_math_villada)

        subject_physics_villada = Subject.objects.create(
            name="Física",
            color='#2980B9',  
            abbreviation="FIS",
            school=school_villada
        )
        subjectsV.append(subject_physics_villada)

        subject_chemistry_villada = Subject.objects.create(
            name="Química",
            color='#27AE60',  
            abbreviation="QUI",
            school=school_villada
        )
        subjectsV.append(subject_chemistry_villada)

        subject_biology_villada = Subject.objects.create(
            name="Biología",
            color='#8E44AD',  
            abbreviation="BIO",
            school=school_villada
        )
        subjectsV.append(subject_biology_villada)

        subject_english_villada = Subject.objects.create(
            name="Inglés",
            color='#F1C40F',  
            abbreviation="ING",
            school=school_villada
        )
        subjectsV.append(subject_english_villada)

        subject_history_villada = Subject.objects.create(
            name="Historia",
            color='#D35400',  
            abbreviation="HIS",
            school=school_villada
        )
        subjectsV.append(subject_history_villada)

        subject_geography_villada = Subject.objects.create(
            name="Geografía",
            color='#E67E22',  
            abbreviation="GEO",
            school=school_villada
        )
        subjectsV.append(subject_geography_villada)


        subject_literature_villada = Subject.objects.create(
            name="Literatura",
            color='#F39C12',  
            abbreviation="LIT",
            school=school_villada
        )
        subjectsV.append(subject_literature_villada)

        subject_computer_science_villada = Subject.objects.create(
            name="Informática",
            color='#D35400',  
            abbreviation="INF",
            school=school_villada
        )
        subjectsV.append(subject_computer_science_villada)

        subject_art_villada = Subject.objects.create(
            name="Arte",
            color='#8E44AD',  
            abbreviation="ART",
            school=school_villada
        )
        subjectsV.append(subject_art_villada)

        subject_philosophy_villada = Subject.objects.create(

            name="Filosofía",
            color='#27AE60',  
            abbreviation="FIL",
            school=school_villada
        )
        subjectsV.append(subject_philosophy_villada)

        subject_music_villada = Subject.objects.create(
            name="Música",
            color='#F1C40F',  
            abbreviation="MUS",
            school=school_villada
        )

        subjectsV.append(subject_music_villada)

        subject_physical_education_villada = Subject.objects.create(
            name="Educación Física",
            color='#C0392B',  
            abbreviation="EF",
            school=school_villada
        )
        subjectsV.append(subject_physical_education_villada)

        subject_religion_villada = Subject.objects.create(
            name="Religión",
            color='#2980B9',  
            abbreviation="REL",
            school=school_villada
        )
        subjectsV.append(subject_religion_villada)

        subject_electricity_villada = Subject.objects.create(
            name="Electricidad",
            color='#27AE60',  
            abbreviation="ELE",
            school=school_villada
        )
        subjectsV.append(subject_electricity_villada)

        subject_mechanics_villada = Subject.objects.create(
            name="Mecánica",
            color='#8E44AD',  
            abbreviation="MEC",
            school=school_villada
        )
        subjectsV.append(subject_mechanics_villada)



        # Asignar materias a los cursos de Villada
        coursesubjectsV = []
        for j, subject in enumerate(subjectsV):
            for i, course in enumerate(courses_villada):
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(
                    studyPlan=studyPlan, subject=subject, course=course, weeklyHours=5
                )
                coursesubjectsV.append(coursesubject)
        print(len(coursesubjectsV))




        # Asignar materias a los profesores de Villada
        subject_per_teacher = 12
        # TSS Villada
        for i, coursesubject in enumerate(coursesubjectsV):
            # Determinar el profesor actual usando división entera
            teacher = teacherV[(i // subject_per_teacher) % len(teacherV)]
            TeacherSubjectSchool.objects.create(
                school=school_villada,
                coursesubjects=coursesubject,
                teacher=teacher
            )



        # Eventos para Villada
        event_villada_1 = Event.objects.create(
            name='Reunión pedagógica',
            startDate=timezone.now(),
            endDate=timezone.now() + timedelta(hours=3),
            school=school_villada,
            eventType=event_type4
        )
        event_villada_1.roles.add(role_directive, role_teacher)
        event_villada_1.affiliated_teachers.add(teacher_math_villada)

        event_villada_2 = Event.objects.create(
            name='Excursión al museo histórico',
            startDate=timezone.now() + timedelta(days=7),
            endDate=timezone.now() + timedelta(days=7, hours=6),
            school=school_villada,
            eventType=event_type1
        )
        event_villada_2.roles.add(role_teacher, role_preceptor)
        event_villada_2.affiliated_teachers.add(teacher_math_villada)

        event_villada_3 = Event.objects.create(
            name='Taller de actualización docente en programación',
            startDate=timezone.now() + timedelta(days=2),
            endDate=timezone.now() + timedelta(days=2, hours=4),
            school=school_villada,
            eventType=event_type4
        )
        event_villada_3.roles.add(role_teacher)
        event_villada_3.affiliated_teachers.add(teacher_computer_science_villada)

        event_villada_4 = Event.objects.create(
            name='Revisión técnica de laboratorios',
            startDate=timezone.now() + timedelta(days=5),
            endDate=timezone.now() + timedelta(days=5, hours=3),
            school=school_villada,
            eventType=event_type5
        )
        event_villada_4.roles.add(role_directive)

        event_villada_5 = Event.objects.create(
            name='Jornada de integración estudiantil',
            startDate=timezone.now() + timedelta(days=10),
            endDate=timezone.now() + timedelta(days=10, hours=6),
            school=school_villada,
            eventType=event_type
        )
        event_villada_5.roles.add(role_teacher, role_preceptor)

        event_villada_6 = Event.objects.create(
            name='Simulacro de evacuación',
            startDate=timezone.now() + timedelta(days=3),
            endDate=timezone.now() + timedelta(days=3, hours=1),
            school=school_villada,
            eventType=event_type5
        )
        event_villada_6.roles.add(role_directive, role_teacher, role_preceptor)

        event_villada_7 = Event.objects.create(
            name='Paro de transporte',
            startDate=timezone.now() + timedelta(days=14),
            endDate=timezone.now() + timedelta(days=14, hours=8),
            school=school_villada,
            eventType=event_type1
        )
        event_villada_7.roles.add(role_directive)

        event_villada_8 = Event.objects.create(
            name='Excursión al centro de ciencias',
            startDate=timezone.now() + timedelta(days=12),
            endDate=timezone.now() + timedelta(days=12, hours=7),
            school=school_villada,
            eventType=event_type2
        )
        event_villada_8.roles.add(role_teacher)
        event_villada_8.affiliated_teachers.add(teacher_physics_villada, teacher_biology_villada)

        event_villada_9 = Event.objects.create(
            name='Reunión del consejo escolar',
            startDate=timezone.now() + timedelta(days=8),
            endDate=timezone.now() + timedelta(days=8, hours=4),
            school=school_villada,
            eventType=event_type
        )
        event_villada_9.roles.add(role_directive)

        event_villada_10 = Event.objects.create(
            name='Capacitación docente en robótica',
            startDate=timezone.now() + timedelta(days=6),
            endDate=timezone.now() + timedelta(days=6, hours=5),
            school=school_villada,
            eventType=event_type4
        )
        event_villada_10.roles.add(role_teacher)
        event_villada_10.affiliated_teachers.add(teacher_mechanics_villada, teacher_computer_science_villada)

        event_villada_11 = Event.objects.create(
            name='Mantenimiento de la sala de informática',
            startDate=timezone.now() + timedelta(days=9),
            endDate=timezone.now() + timedelta(days=9, hours=3),
            school=school_villada,
            eventType=event_type5
        )
        event_villada_11.roles.add(role_directive)

        event_villada_12 = Event.objects.create(
            name='Taller de primeros auxilios',
            startDate=timezone.now() + timedelta(days=4),
            endDate=timezone.now() + timedelta(days=4, hours=4),
            school=school_villada,
            eventType=event_type4
        )
        event_villada_12.roles.add(role_teacher)
        event_villada_12.affiliated_teachers.add(teacher_math_villada, teacher_chemistry_villada)

        event_villada_13 = Event.objects.create(
            name='Charlas sobre ética profesional',
            startDate=timezone.now() + timedelta(days=11),
            endDate=timezone.now() + timedelta(days=11, hours=3),
            school=school_villada,
            eventType=event_type4
        )
        event_villada_13.roles.add(role_teacher)
        event_villada_13.affiliated_teachers.add(teacher_philosophy_villada, teacher_literature_villada)

        event_villada_14 = Event.objects.create(
            name='Paro docente general',
            startDate=timezone.now() + timedelta(days=20),
            endDate=timezone.now() + timedelta(days=20, hours=8),
            school=school_villada,
            eventType=event_type3
        )
        event_villada_14.roles.add(role_teacher)

        event_villada_15 = Event.objects.create(
            name='Visita guiada al parque industrial',
            startDate=timezone.now() + timedelta(days=18),
            endDate=timezone.now() + timedelta(days=18, hours=6),
            school=school_villada,
            eventType=event_type2
        )
        event_villada_15.roles.add(role_teacher)
        event_villada_15.affiliated_teachers.add(teacher_mechanics_villada, teacher_electricity_villada)

        event_villada_16 = Event.objects.create(
            name='Exposición de proyectos técnicos',
            startDate=timezone.now() + timedelta(days=15),
            endDate=timezone.now() + timedelta(days=15, hours=5),
            school=school_villada,
            eventType=event_type
        )
        event_villada_16.roles.add(role_teacher, role_preceptor)
        event_villada_16.affiliated_teachers.add(teacher_computer_science_villada, teacher_art_villada)

        event_villada_17 = Event.objects.create(
            name='Jornada de concientización ambiental',
            startDate=timezone.now() + timedelta(days=19),
            endDate=timezone.now() + timedelta(days=19, hours=4),
            school=school_villada,
            eventType=event_type
        )
        event_villada_17.roles.add(role_teacher)
        event_villada_17.affiliated_teachers.add(teacher_geography_villada, teacher_biology_villada)


        #disponibilidad de los profesores de Vill
        for j, teacher in enumerate(teacherV):
            for i, module in enumerate(modules_villada):
                availabilityState = available if i % 3 < 2 else not_available
                TeacherAvailability.objects.create(
                    module=module,
                    teacher=teacher,
                    loadDate=datetime.now(),
                    availabilityState=availabilityState
                )

