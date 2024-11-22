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

        contact_info_preceptor_4to_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Salta',
            streetNumber='900',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_5to_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Córdoba',
            streetNumber='1000',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_preceptor_6to_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Santa',
            streetNumber='1100',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_lasalle = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Lorenzo',
            streetNumber='500',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_physics = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Lorenzo',
            streetNumber='501',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_math = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Lorenzo',
            streetNumber='502',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_chemistry = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Mendoza',
            streetNumber='503',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_biology = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Mendoza',
            streetNumber='504',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_english = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Córdoba',
            streetNumber='505',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_history = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Córdoba',
            streetNumber='506',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_geography = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Entre Ríos',
            streetNumber='507',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_literature = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle 9 de Julio',
            streetNumber='508',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_computer_science = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle San Martín',
            streetNumber='509',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_art = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Salta',
            streetNumber='510',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_philosophy = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Catamarca',
            streetNumber='511',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_music = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Entre Ríos',
            streetNumber='512',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_physical_education = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Santiago',
            streetNumber='513',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_religion = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle La Rioja',
            streetNumber='514',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )

        contact_info_french = ContactInformation.objects.create(
            postalCode='4004',
            street='Calle Mendoza',
            streetNumber='515',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )


        directives = []

        # Director Lasalle
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
        directives.append(directive_lasalle)

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

        preceptor_3ro_lasalle = CustomUser.objects.create_user(
            email='preceptor3ro@lasalle.edu',
            password='password',
            first_name='Verónica',
            last_name='Giménez',
            gender='femenino',
            document='22345003',
            profile_picture=defaultuser,
            hoursToWork=22,
            phone='3816109876',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_3ro_lasalle,
            email_verified=True
        )

        preceptor_4to_lasalle = CustomUser.objects.create_user(
            email='preceptor4to@lasalle.edu',
            password='password',
            first_name='Martín',
            last_name='Peralta',
            gender='masculino',
            document='22345004',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3816112345',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_4to_lasalle,
            email_verified=True
        )

        preceptor_5to_lasalle = CustomUser.objects.create_user(
            email='preceptor5to@lasalle.edu',
            password='password',
            first_name='Gabriela',
            last_name='Salas',
            gender='femenino',
            document='22345005',
            profile_picture=defaultuser,
            hoursToWork=18,
            phone='3816123456',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_5to_lasalle,
            email_verified=True
        )


        preceptor_6to_lasalle = CustomUser.objects.create_user(
            email='preceptor6to@lasalle.edu',
            password='password',
            first_name='Francisco',
            last_name='Ledesma',
            gender='masculino',
            document='22345006',
            profile_picture=defaultuser,
            hoursToWork=19,
            phone='3816134567',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_6to_lasalle,
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
            contactInfo=contact_info_physics,
            email_verified=True
        )
        teacherLS.append(teacher_physics_lasalle)

        teacher_math_lasalle = CustomUser.objects.create_user(
            email='math@lasalle.edu',
            password='password',
            first_name='Sofía',
            last_name='López',
            gender='femenino',
            document='67890124',
            profile_picture=defaultuser,
            hoursToWork=28,
            phone='3816701135',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_math,
            email_verified=True
        )
        teacherLS.append(teacher_math_lasalle)

        teacher_chemistry_lasalle = CustomUser.objects.create_user(
            email='chemistry@lasalle.edu',
            password='password',
            first_name='Daniel',
            last_name='Romero',
            gender='masculino',
            document='67890125',
            profile_picture=defaultuser,
            hoursToWork=24,
            phone='3816701136',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_chemistry,
            email_verified=True
        )
        teacherLS.append(teacher_chemistry_lasalle)

        teacher_biology_lasalle = CustomUser.objects.create_user(
            email='biology@lasalle.edu',
            password='password',
            first_name='Carla',
            last_name='Gutiérrez',
            gender='femenino',
            document='67890126',
            profile_picture=defaultuser,
            hoursToWork=26,
            phone='3816701137',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_biology,
            email_verified=True
        )
        teacherLS.append(teacher_biology_lasalle)

        teacher_english_lasalle = CustomUser.objects.create_user(
            email='english@lasalle.edu',
            password='password',
            first_name='Lucía',
            last_name='Fernández',
            gender='femenino',
            document='67890127',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3816701138',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_english,
            email_verified=True
        )
        teacherLS.append(teacher_english_lasalle)

        
        teacher_history_lasalle = CustomUser.objects.create_user(
            email='history@lasalle.edu',
            password='password',
            first_name='Marcos',
            last_name='Vargas',
            gender='masculino',
            document='67890128',
            profile_picture=defaultuser,
            hoursToWork=27,
            phone='3816701139',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_history,
            email_verified=True
        )
        teacherLS.append(teacher_history_lasalle)


        
        teacher_geography_lasalle = CustomUser.objects.create_user(
            email='geography@lasalle.edu',
            password='password',
            first_name='Laura',
            last_name='Guzmán',
            gender='femenino',
            document='67890129',
            profile_picture=defaultuser,
            hoursToWork=26,
            phone='3816701140',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_geography,
            email_verified=True
        )
        teacherLS.append(teacher_geography_lasalle)

        teacher_literature_lasalle = CustomUser.objects.create_user(
            email='literature@lasalle.edu',
            password='password',
            first_name='Diana',
            last_name='Sosa',
            gender='femenino',
            document='67890130',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3816701141',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_literature,
            email_verified=True
        )
        teacherLS.append(teacher_literature_lasalle)

        teacher_computer_science_lasalle = CustomUser.objects.create_user(
            email='computerscience@lasalle.edu',
            password='password',
            first_name='Mario',
            last_name='González',
            gender='masculino',
            document='67890131',
            profile_picture=defaultuser,
            hoursToWork=25,
            phone='3816701142',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_computer_science,
            email_verified=True
        )
        teacherLS.append(teacher_computer_science_lasalle)

        teacher_art_lasalle = CustomUser.objects.create_user(
            email='art@lasalle.edu',
            password='password',
            first_name='Clara',
            last_name='Espinoza',
            gender='femenino',
            document='67890132',
            profile_picture=defaultuser,
            hoursToWork=18,
            phone='3816701143',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_art,
            email_verified=True
        )
        teacherLS.append(teacher_art_lasalle)

        teacher_philosophy_lasalle = CustomUser.objects.create_user(
            email='philosophy@lasalle.edu',
            password='password',
            first_name='Fernando',
            last_name='Álvarez',
            gender='masculino',
            document='67890133',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3816701144',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_philosophy,
            email_verified=True
        )
        teacherLS.append(teacher_philosophy_lasalle)

        teacher_music_lasalle = CustomUser.objects.create_user(
            email='music@lasalle.edu',
            password='password',
            first_name='Julia',
            last_name='Roldán',
            gender='femenino',
            document='67890134',
            profile_picture=defaultuser,
            hoursToWork=24,
            phone='3816701145',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_music,
            email_verified=True
        )
        teacherLS.append(teacher_music_lasalle)

        teacher_physical_education_lasalle = CustomUser.objects.create_user(
            email='physicaleducation@lasalle.edu',
            password='password',
            first_name='Andrés',
            last_name='Paredes',
            gender='masculino',
            document='67890135',
            profile_picture=defaultuser,
            hoursToWork=28,
            phone='3816701146',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_physical_education,
            email_verified=True
        )
        teacherLS.append(teacher_physical_education_lasalle)

        teacher_religion_lasalle = CustomUser.objects.create_user(
            email='religion@lasalle.edu',
            password='password',
            first_name='Camila',
            last_name='Herrera',
            gender='femenino',
            document='67890136',
            profile_picture=defaultuser,
            hoursToWork=22,
            phone='3816701147',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_religion,
            email_verified=True
        )
        teacherLS.append(teacher_religion_lasalle)

        teacher_french_lasalle = CustomUser.objects.create_user(
            email='french@lasalle.edu',
            password='password',
            first_name='Luis',
            last_name='Dupont',
            gender='masculino',
            document='67890137',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3816701148',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_french,
            email_verified=True
        )
        teacherLS.append(teacher_french_lasalle)


        # Crear escuela Lasalle
        school_lasalle = School.objects.create(
            name='Lasalle',
            abbreviation='LAS',
            logo=logolasalle,  # Define este logotipo en seed_images.py
            email='contacto@lasalle.edu',
            contactInfo=contact_info_lasalle
        )

        #Modulos de Lasalle
        days_of_week = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
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
        
        #año de lasalle
        year1_lasalle = Year.objects.create(name='1er Año', number='1', school=school_lasalle)
        year2_lasalle = Year.objects.create(name='2do Año', number='2', school=school_lasalle)
        year3_lasalle = Year.objects.create(name='3er Año', number='3', school=school_lasalle)
        year4_lasalle = Year.objects.create(name='4to Año', number='4', school=school_lasalle)
        year5_lasalle = Year.objects.create(name='5to Año', number='5', school=school_lasalle)
        year6_lasalle = Year.objects.create(name='6to Año', number='6', school=school_lasalle)


       # Crear cursos para Lasalle
        course_names = ['A', 'B', 'C']
        courses_lasalle = []
        for year in [year1_lasalle, year2_lasalle, year3_lasalle, year4_lasalle, year5_lasalle, year6_lasalle]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                courses_lasalle.append(course)


        # Materias de Lasalle
        subjectsLS = []
        subject_math_lasalle = Subject.objects.create(
            name="Matemáticas",
            color='#C0392B',  
            abbreviation="MAT",
            school=school_lasalle
        )
        subjectsLS.append(subject_math_lasalle)

        subject_physics_lasalle = Subject.objects.create(
            name="Física",
            color='#2980B9',  
            abbreviation="FIS",
            school=school_lasalle
        )
        subjectsLS.append(subject_physics_lasalle)

        subject_chemistry_lasalle = Subject.objects.create(
            name="Química",
            color='#27AE60',  
            abbreviation="QUI",
            school=school_lasalle
        )
        subjectsLS.append(subject_chemistry_lasalle)

        subject_biology_lasalle = Subject.objects.create(
            name="Biología",
            color='#8E44AD',  
            abbreviation="BIO",
            school=school_lasalle
        )
        subjectsLS.append(subject_biology_lasalle)

        subject_english_lasalle = Subject.objects.create(
            name="Inglés",
            color='#F1C40F',  
            abbreviation="ING",
            school=school_lasalle
        )
        subjectsLS.append(subject_english_lasalle)

        subject_history_lasalle = Subject.objects.create(
            name="Historia",
            color='#D35400',  
            abbreviation="HIS",
            school=school_lasalle
        )
        subjectsLS.append(subject_history_lasalle)

        subject_geography_lasalle = Subject.objects.create(
            name="Geografía",
            color='#3498DB',  
            abbreviation="GEO",
            school=school_lasalle
        )
        subjectsLS.append(subject_geography_lasalle)

        subject_literature_lasalle = Subject.objects.create(
            name="Literatura",
            color='#9B59B6',  
            abbreviation="LIT",
            school=school_lasalle
        )

        subjectsLS.append(subject_literature_lasalle)

        subject_computer_science_lasalle = Subject.objects.create(
            name="Informática",
            color='#1ABC9C',  
            abbreviation="INF",
            school=school_lasalle
        )
        subjectsLS.append(subject_computer_science_lasalle)

        subject_art_lasalle = Subject.objects.create(
            name="Arte",
            color='#E74C3C',  
            abbreviation="ART",
            school=school_lasalle
        )
        subjectsLS.append(subject_art_lasalle)

        subject_philosophy_lasalle = Subject.objects.create(
            name="Filosofía",
            color='#F39C12',  
            abbreviation="FIL",
            school=school_lasalle
        )
        subjectsLS.append(subject_philosophy_lasalle)

        subject_music_lasalle = Subject.objects.create(
            name="Música",
            color='#3498DB',  
            abbreviation="MUS",
            school=school_lasalle
        )
        subjectsLS.append(subject_music_lasalle)

        subject_physical_education_lasalle = Subject.objects.create(
            name="Educación Física",
            color='#27AE60',  
            abbreviation="EF",
            school=school_lasalle
        )
        subjectsLS.append(subject_physical_education_lasalle)

        subject_religion_lasalle = Subject.objects.create(
            name="Religión",
            color='#8E44AD',  
            abbreviation="REL",
            school=school_lasalle
        )
        subjectsLS.append(subject_religion_lasalle)

        subject_french_lasalle = Subject.objects.create(
            name="Francés",
            color='#D35400',  
            abbreviation="FRA",
            school=school_lasalle
        )
        subjectsLS.append(subject_french_lasalle)





        # Asignar materias a los cursos de Lasalle
        coursesubjectsLS = []
        for j, subject in enumerate(subjectsLS):
            for i, course in enumerate(courses_lasalle):
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(
                    studyPlan=studyPlan, subject=subject, course=course, weeklyHours=5
                )
                coursesubjectsLS.append(coursesubject)
        print(len(coursesubjectsLS))


        # Asignar profesores a las materias de Lasalle
        subjects_per_teacher = 12
        # TSS LS
        for i,coursesubject in enumerate(coursesubjectsLS):
            teacher = teacherLS[(i // subjects_per_teacher) % len(teacherLS)]
            TeacherSubjectSchool.objects.create(
                school=school_lasalle,
                coursesubjects=coursesubject,
                teacher=teacher
            )


        # Crear eventos para Lasalle
        event_lasalle_1 = Event.objects.create(
            name='Capacitación docente en tecnología',
            startDate=timezone.now(),
            endDate=timezone.now() + timedelta(hours=4),
            school=school_lasalle,
            eventType=event_type4
        )
        event_lasalle_1.roles.add(role_directive, role_teacher)
        event_lasalle_1.affiliated_teachers.add(teacher_physics_lasalle)

        event_lasalle_2 = Event.objects.create(
            name='Mantenimiento de la biblioteca',
            startDate=timezone.now() + timedelta(days=3),
            endDate=timezone.now() + timedelta(days=3, hours=5),
            school=school_lasalle,
            eventType=event_type5
        )
        event_lasalle_2.roles.add(role_directive)

        event_lasalle_3 = Event.objects.create(
            name='Reunión de padres',
            startDate=timezone.now() + timedelta(days=5),
            endDate=timezone.now() + timedelta(days=5, hours=2),
            school=school_lasalle,
            eventType=event_type
        )
        event_lasalle_3.roles.add(role_directive)

        # Crear eventos para Lasalle
        event_lasalle_4 = Event.objects.create(
            name='Viaje de estudio a las montañas',
            startDate=timezone.now() + timedelta(days=7),
            endDate=timezone.now() + timedelta(days=10, hours=18),
            school=school_lasalle,
            eventType=event_type2
        )
        event_lasalle_4.roles.add(role_teacher)
        event_lasalle_4.affiliated_teachers.add(teacher_geography_lasalle, teacher_biology_lasalle)

        event_lasalle_5 = Event.objects.create(
            name='Capacitación en primeros auxilios',
            startDate=timezone.now() + timedelta(days=2),
            endDate=timezone.now() + timedelta(days=2, hours=6),
            school=school_lasalle,
            eventType=event_type4
        )
        event_lasalle_5.roles.add(role_teacher)
        event_lasalle_5.affiliated_teachers.add(teacher_physical_education_lasalle, teacher_art_lasalle)

        event_lasalle_6 = Event.objects.create(
            name='Reparación del techo del gimnasio',
            startDate=timezone.now() + timedelta(days=4),
            endDate=timezone.now() + timedelta(days=4, hours=8),
            school=school_lasalle,
            eventType=event_type5
        )
        event_lasalle_6.roles.add(role_directive)

        event_lasalle_7 = Event.objects.create(
            name='Reunión general del consejo escolar',
            startDate=timezone.now() + timedelta(days=1),
            endDate=timezone.now() + timedelta(days=1, hours=3),
            school=school_lasalle,
            eventType=event_type
        )
        event_lasalle_7.roles.add(role_directive, role_teacher)

        event_lasalle_8 = Event.objects.create(
            name='Charla sobre orientación vocacional',
            startDate=timezone.now() + timedelta(days=9),
            endDate=timezone.now() + timedelta(days=9, hours=2),
            school=school_lasalle,
            eventType=event_type4
        )
        event_lasalle_8.roles.add(role_teacher)
        event_lasalle_8.affiliated_teachers.add(teacher_english_lasalle, teacher_literature_lasalle)

        event_lasalle_9 = Event.objects.create(
            name='Visita de inspección del ministerio de educación',
            startDate=timezone.now() + timedelta(days=15),
            endDate=timezone.now() + timedelta(days=15, hours=4),
            school=school_lasalle,
            eventType=event_type
        )
        event_lasalle_9.roles.add(role_directive)

        event_lasalle_10 = Event.objects.create(
            name='Paro docente general',
            startDate=timezone.now() + timedelta(days=20),
            endDate=timezone.now() + timedelta(days=20, hours=8),
            school=school_lasalle,
            eventType=event_type3
        )
        event_lasalle_10.roles.add(role_teacher)

        event_lasalle_11 = Event.objects.create(
            name='Excursión al museo histórico',
            startDate=timezone.now() + timedelta(days=12),
            endDate=timezone.now() + timedelta(days=12, hours=5),
            school=school_lasalle,
            eventType=event_type2
        )
        event_lasalle_11.roles.add(role_teacher)
        event_lasalle_11.affiliated_teachers.add(teacher_history_lasalle, teacher_geography_lasalle)

        event_lasalle_12 = Event.objects.create(
            name='Día de integración escolar',
            startDate=timezone.now() + timedelta(days=14),
            endDate=timezone.now() + timedelta(days=14, hours=6),
            school=school_lasalle,
            eventType=event_type
        )
        event_lasalle_12.roles.add(role_directive, role_teacher, role_preceptor)
        event_lasalle_12.affiliated_teachers.add(
            teacher_philosophy_lasalle,
            teacher_physical_education_lasalle,
            teacher_music_lasalle
        )

        event_lasalle_13 = Event.objects.create(
            name='Capacitación en herramientas digitales',
            startDate=timezone.now() + timedelta(days=18),
            endDate=timezone.now() + timedelta(days=18, hours=5),
            school=school_lasalle,
            eventType=event_type4
        )
        event_lasalle_13.roles.add(role_teacher)
        event_lasalle_13.affiliated_teachers.add(teacher_computer_science_lasalle, teacher_art_lasalle)

        # Disponibilidad de los profesores de Lasalle
        for j, teacher in enumerate(teacherLS):
            for i, module in enumerate(modules_lasalle):
                availabilityState = available if i % 3 < 2 else not_available
                TeacherAvailability.objects.create(
                    module=module,
                    teacher=teacher,
                    loadDate=datetime.now(),
                    availabilityState=availabilityState
                )