from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event, Role, CourseSubjects
)
import uuid
from django.utils import timezone
from datetime import time, timedelta, datetime
from .seed_images import *
class Command(BaseCommand):
    help = 'Seed database with initial data'
    # python manage.py seed
    def handle(self, *args, **options):
        # Crear tipos de documentos
        dni = DocumentType.objects.create(name="DNI", description="Documento Nacional de Identidad")
        passport = DocumentType.objects.create(name="Pasaporte", description="Documento de viaje internacional")
        cuit = DocumentType.objects.create(name="CUIT", description="CUIT")

        # Crear nacionalidades
        argentina = Nationality.objects.create(name="Argentina", description="Nacionalidad argentina")
        uruguay = Nationality.objects.create(name="Uruguay", description="Nacionalidad uruguaya")
        brasil = Nationality.objects.create(name="Brasil", description="Nacionalidad brasileña")
        paraguay = Nationality.objects.create(name="Paraguay", description="Nacionalidad paraguaya")
        chile = Nationality.objects.create(name="Chile", description="Nacionalidad chilena")
        bolivia = Nationality.objects.create(name="Bolivia", description="Nacionalidad boliviana")
        peru = Nationality.objects.create(name="Perú", description="Nacionalidad peruana")
        otros = Nationality.objects.create(name="Otros", description="Nacionalidad otros")


        # Crear ContactInformation
        # Directivo
        contact_info_directive = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle Nash',
            streetNumber='294',
            city='Córdoba',
            province='Córdoba'
        )
        # Información de contacto para cada profesor
        contact_info_matematica = ContactInformation.objects.create(
            postalCode='5001',
            street='Calle San Jerónimo',
            streetNumber='101',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_fisica = ContactInformation.objects.create(
            postalCode='5002',
            street='Calle Obispo Trejo',
            streetNumber='102',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_quimica = ContactInformation.objects.create(
            postalCode='5003',
            street='Calle Vélez Sarsfield',
            streetNumber='103',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_biologia = ContactInformation.objects.create(
            postalCode='5004',
            street='Calle 9 de Julio',
            streetNumber='104',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_ingles = ContactInformation.objects.create(
            postalCode='5005',
            street='Avenida Olmos',
            streetNumber='105',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_educacion_fisica = ContactInformation.objects.create(
            postalCode='5006',
            street='Avenida General Paz',
            streetNumber='106',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_religion = ContactInformation.objects.create(
            postalCode='5007',
            street='Calle Ituzaingó',
            streetNumber='107',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_latin = ContactInformation.objects.create(
            postalCode='5008',
            street='Calle Tucumán',
            streetNumber='108',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_geografia = ContactInformation.objects.create(
            postalCode='5009',
            street='Avenida Maipú',
            streetNumber='109',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_lengua = ContactInformation.objects.create(
            postalCode='5010',
            street='Calle Belgrano',
            streetNumber='110',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info_informatica = ContactInformation.objects.create(
            postalCode='5025',
            street='Avenida del Trabajo',
            streetNumber='250',
            city='Córdoba',
            province='Córdoba'
        )

        # Preceptores por año
        contact_info_preceptor_1ro = ContactInformation.objects.create(
            postalCode='5000',
            street='Avenida Colón',
            streetNumber='2345',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info_preceptor_2do = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle Duarte Quiros',
            streetNumber='3456',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info_preceptor_3ro = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle La Rioja',
            streetNumber='4567',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info_preceptor_4to = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle Catamarca',
            streetNumber='5678',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info_preceptor_5to = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle Mendoza',
            streetNumber='6789',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info_preceptor_6to = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle Entre Ríos',
            streetNumber='7890',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info14 = ContactInformation.objects.create(
            postalCode='4000',
            street='Calle San Martín',
            streetNumber='101',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )
       

        # Crear escuela
        school = School.objects.create(
            name='Jesús María',
            abbreviation='JM',
            logo= logojesusmaria,
            email='contacto@jesusmaria.edu',
            contactInfo=contact_info14
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
            contactInfo=contact_info_directive
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
            contactInfo=contact_info_matematica
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
            contactInfo=contact_info_fisica
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
            contactInfo=contact_info_quimica
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
            contactInfo=contact_info_biologia
        )
        teacherJM.append(teacher_biologia)

        teacher_ingles = CustomUser.objects.create_user(
            email='ingles@secundaria.edu',
            password='password',
            first_name='Daniel',
            last_name='Suárez',
            gender='masculino',
            document='56789012',
            profile_picture=defaultuser,
            hoursToWork=18,
            phone='3516701128',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_ingles
        )
        teacherJM.append(teacher_ingles)

        teacher_educacion_fisica = CustomUser.objects.create_user(
            email='educacionfisica@secundaria.edu',
            password='password',
            first_name='Lucía',
            last_name='Méndez',
            gender='femenino',
            document='67890123',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3516701129',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_educacion_fisica
        )
        teacherJM.append(teacher_educacion_fisica)

        teacher_religion = CustomUser.objects.create_user(
            email='religion@secundaria.edu',
            password='password',
            first_name='José',
            last_name='Aguilar',
            gender='masculino',
            document='78901234',
            profile_picture=defaultuser,
            hoursToWork=15,
            phone='3516701130',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_religion
        )
        teacherJM.append(teacher_religion)

        teacher_latin = CustomUser.objects.create_user(
            email='latin@secundaria.edu',
            password='password',
            first_name='Marta',
            last_name='Vázquez',
            gender='femenino',
            document='89012345',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3516701131',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_latin
        )
        teacherJM.append(teacher_latin)

        teacher_geografia = CustomUser.objects.create_user(
            email='geografia@secundaria.edu',
            password='password',
            first_name='Ramiro',
            last_name='Romero',
            gender='masculino',
            document='90123456',
            profile_picture=defaultuser,
            hoursToWork=23,
            phone='3516701132',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_geografia
        )
        teacherJM.append(teacher_geografia)

        teacher_lengua = CustomUser.objects.create_user(
            email='lengua2@secundaria.edu',
            password='password',
            first_name='Clara',
            last_name='Fernández',
            gender='femenino',
            document='15437893',
            profile_picture=defaultuser,
            hoursToWork=25,
            phone='3516701133',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_lengua
        )
        teacherJM.append(teacher_lengua)

        teacher_informatica = CustomUser.objects.create_user(
            email='informatica@secundaria.edu',
            password='password',
            first_name='Luciano',
            last_name='Pereyra',
            gender='masculino',
            document='17894563',
            profile_picture=defaultuser,
            hoursToWork=30,
            phone='3516752234',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_informatica
        )
        teacherJM.append(teacher_informatica)



        # Preceptores
        preceptor_1ro = CustomUser.objects.create_user(
            email='preceptor1ro@secundaria.edu',
            password='password',
            first_name='Andrea',
            last_name='Quiroga',
            gender='femenino',
            document='26789012',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3516701200',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_1ro
        )

        preceptor_2do = CustomUser.objects.create_user(
            email='preceptor2do@secundaria.edu',
            password='password',
            first_name='Miguel',
            last_name='Bustamante',
            gender='masculino',
            document='27890123',
            profile_picture=defaultuser,
            hoursToWork=25,
            phone='3516701211',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_2do
        )
        preceptor_3ro = CustomUser.objects.create_user(
            email='preceptor3ro@secundaria.edu',
            password='password',
            first_name='Lucía',
            last_name='Fernández',
            gender='femenino',
            document='28901234',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3516701222',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_3ro
        )
        preceptor_4to = CustomUser.objects.create_user(
            email='preceptor4to@secundaria.edu',
            password='password',
            first_name='José',
            last_name='Morales',
            gender='masculino',
            document='29012345',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3516701233',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_4to
        )
        preceptor_5to = CustomUser.objects.create_user(
            email='preceptor5to@secundaria.edu',
            password='password',
            first_name='Elena',
            last_name='Ramírez',
            gender='femenino',
            document='30123456',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3516701244',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_5to
        )
        preceptor_6to = CustomUser.objects.create_user(
            email='preceptor6to@secundaria.edu',
            password='password',
            first_name='Ricardo',
            last_name='Guzmán',
            gender='masculino',
            document='31234567',
            profile_picture=defaultuser,
            hoursToWork=20,
            phone='3516701255',
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info_preceptor_6to
        )

        # Asignar directivos a la escuela
        school.directives.add(directive_user)

        # Crear módulos
        days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']
        modulesJM = []
        for i, day in enumerate(days_of_week, start=1):
            for j in range(1, 6):
                module = Module.objects.create(
                    moduleNumber=j,
                    day=day,
                    startTime=time(8 + j, 0),
                    endTime=time(9 + j, 0),
                    school=school
                )
                modulesJM.append(module)
        

        # Crear estados de disponibilidad
        available = AvailabilityState.objects.create(name='Disponible', isEnabled=True)
        not_available = AvailabilityState.objects.create(name='No Disponible', isEnabled=False)
        asigned = AvailabilityState.objects.create(name='Asignado', isEnabled=False)

        # Crear disponibilidad de profesor en Jesús María
        for j, teacher in enumerate(teacherJM):
            for i, module in enumerate(modulesJM):
                availabilityState = available if i % 3 < 2 else not_available
                TeacherAvailability.objects.create(
                    module=module,
                    teacher=teacher,
                    loadDate=datetime.now(),
                    availabilityState=availabilityState
                )

      

        # Crear años JM
        year1 = Year.objects.create(name='1er Año', number='1', school=school)
        year2 = Year.objects.create(name='2do Año', number='2', school=school)
        year3 = Year.objects.create(name='3er Año', number='3', school=school)
        year4 = Year.objects.create(name='4to Año', number='4', school=school)
        year5 = Year.objects.create(name='5to Año', number='5', school=school)
        year6 = Year.objects.create(name='6to Año', number='6', school=school)

        year1.preceptors.add(preceptor_1ro)
        year2.preceptors.add(preceptor_2do)
        year3.preceptors.add(preceptor_3ro)
        year4.preceptors.add(preceptor_4to)
        year5.preceptors.add(preceptor_5to)
        year6.preceptors.add(preceptor_6to)


        # Crear Curso
        course_names = ['A', 'B', 'C']

        # Crear cursos para los años de Jesús María
        coursesJM = []
        for year in [year1, year2, year3, year4, year5, year6]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                coursesJM.append(course)


        # Crear materias JM
        subjectsJM = []
        subject1 = Subject.objects.create(
            name="Matemáticas",
            color='#C0392B',  
            abbreviation="MAT",
            school=school
        )
        subjectsJM.append(subject1)

        subject2 = Subject.objects.create(
            name="Física",
            color='#2980B9',  
            abbreviation="FIS",
            school=school
        )
        subjectsJM.append(subject2)

        subject3 = Subject.objects.create(
            name="Química",
            color='#8E44AD',  
            abbreviation="QUI",
            school=school
        )
        subjectsJM.append(subject3)

        subject4 = Subject.objects.create(
            name="Biología",
            color='#27AE60',  
            abbreviation="BIO",
            school=school
        )
        subjectsJM.append(subject4)

        subject5 = Subject.objects.create(
            name="Inglés",
            color='#F39C12',  
            abbreviation="ING",
            school=school
        )
        subjectsJM.append(subject5)

        subject6 = Subject.objects.create(
            name="Educación Física",
            color='#F39C12',  
            abbreviation="EDF",
            school=school
        )
        subjectsJM.append(subject6)

        subject7 = Subject.objects.create(
            name="Religión",
            color='#F39C12',  
            abbreviation="REL",
            school=school
        )
        subjectsJM.append(subject7)

        subject8 = Subject.objects.create(
            name="Lengua",
            color='#F39C12',  
            abbreviation="LEN",
            school=school
        )
        subjectsJM.append(subject8)

        subject9 = Subject.objects.create(
            name="Latín",
            color='#F39C12',  
            abbreviation="LAT",
            school=school
        )
        subjectsJM.append(subject9)

        subject10 = Subject.objects.create(
            name="Geografía",
            color='#F39C12',  
            abbreviation="GEO",
            school=school
        )
        subjectsJM.append(subject10)

        subject11 = Subject.objects.create(
            name="Informatica",
            color='#F39C12',  
            abbreviation="INF",
            school=school
        )
        subjectsJM.append(subject11)



        # Asignar materias a cursos
        coursesubjectJM = []
        for j, subject in enumerate(subjectsJM):
            for i, course in enumerate(coursesJM):
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(studyPlan=studyPlan, subject=subject, course=course, weeklyHours=5)
                coursesubjectJM.append(coursesubject)
        print(len(coursesubjectJM))


        # Asignar profesor a materia en una escuela
        subjects_per_teacher = 12
        # TSS JM
        for i, coursesubject in enumerate(coursesubjectJM):
            # Determinar el profesor actual usando división entera
            teacher = teacherJM[(i // subjects_per_teacher) % len(teacherJM)]
            TeacherSubjectSchool.objects.create(
                school=school,
                coursesubjects=coursesubject,
                teacher=teacher
            )

        
        # Crear acciones
        action1 = Action.objects.create(name='Agregar materia', isEnabled=True)
        action2 = Action.objects.create(name='Cambiar materia', isEnabled=False)


        # Crear tipos de eventos
        event_type1 = EventType.objects.create(name='Paro de transporte', description='Interrupción de servicios de transporte')
        event_type2 = EventType.objects.create(name='Viaje escolar', description='Excursión organizada por la escuela')
        event_type3 = EventType.objects.create(name='Paro docente', description='Paro de docentes')
        event_type4 = EventType.objects.create(name='Taller Docente', description='Dictado de taller docente')
        event_type5 = EventType.objects.create(name='Mantenimiento Infraestructura', description='realizacion de mantenimiento en el instituto')
        event_type = EventType.objects.create(name='Otro', description='Otro tipo de evento')
        
        # Crear roles
        directive_role = Role.objects.create(name='Directivo')
        teacher_role = Role.objects.create(name='Profesor')
        preceptor_role = Role.objects.create(name='Preceptor')

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


        #-----------------------------------------------------------------------------------------------------------------------------------------------
        #Seed Villada
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
            contactInfo=contact_info_directive_villada
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
            contactInfo=contact_info_directive_lasalle
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
            contactInfo=contact_info_preceptor_1ro_villada
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
            contactInfo=contact_info_preceptor_2do_villada
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
            contactInfo=contact_info_preceptor_1ro_lasalle
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
            contactInfo=contact_info_preceptor_2do_lasalle
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
            logo=logovillada,  # Define este logotipo en seed_images.py
            email='contacto@villada.edu',
            contactInfo=contact_info_villada
        )

        # Crear escuela Lasalle
        school_lasalle = School.objects.create(
            name='Lasalle',
            abbreviation='LAS',
            logo=logolasalle,  # Define este logotipo en seed_images.py
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
            contactInfo=contact_info_villada
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
            contactInfo=contact_info_lasalle
        )

        # Asignar profesor a materia en Lasalle
        TeacherSubjectSchool.objects.create(
            school=school_lasalle,
            coursesubjects=coursesubjects_lasalle[1],  # Primer curso de Física
            teacher=teacher_physics_lasalle
        )

        # Tipos de eventos compartidos
        event_type_meeting = EventType.objects.create(
            name='Reunión General',
            description='Reunión de directivos y docentes'
        )

        event_type_trip = EventType.objects.create(
            name='Excursión',
            description='Viaje escolar'
        )

        event_type_maintenance = EventType.objects.create(
            name='Mantenimiento',
            description='Revisión de infraestructura escolar'
        )

        # Roles para los eventos
        role_directive = Role.objects.create(name='Directivo')
        role_teacher = Role.objects.create(name='Profesor')
        role_preceptor = Role.objects.create(name='Preceptor')

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

        # Disponibilidad de profesores en Villada
        available = AvailabilityState.objects.create(name='Disponible', isEnabled=True)
        not_available = AvailabilityState.objects.create(name='No Disponible', isEnabled=False)

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

        # Acciones para ambos colegios
        action_add_subject = Action.objects.create(name='Agregar materia', isEnabled=True)
        action_schedule_event = Action.objects.create(name='Programar evento', isEnabled=True)

        school_villada.actions.add(action_add_subject, action_schedule_event)
        school_lasalle.actions.add(action_add_subject, action_schedule_event)

        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))