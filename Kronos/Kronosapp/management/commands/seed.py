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


        # Crear ContactInformation
        contact_info1 = ContactInformation.objects.create(
            postalCode='5000',
            street='Calle Principal',
            streetNumber='123',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info2 = ContactInformation.objects.create(
            postalCode='2000',
            street='Avenida Libertad',
            streetNumber='456',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info3 = ContactInformation.objects.create(
            postalCode='3000',
            street='Boulevard Mitre',
            streetNumber='789',
            city='Santa Fe',
            province='Santa Fe'
        )
        contact_info4 = ContactInformation.objects.create(
            postalCode='4000',
            street='Calle San Martín',
            streetNumber='101',
            city='San Miguel de Tucumán',
            province='Tucumán'
        )
        contact_info5 = ContactInformation.objects.create(
            postalCode='6000',
            street='Avenida Belgrano',
            streetNumber='202',
            city='Salta',
            province='Salta'
        )
        contact_info6 = ContactInformation.objects.create(
            postalCode='7000',
            street='Calle Rivadavia',
            streetNumber='303',
            city='Bahía Blanca',
            province='Buenos Aires'
        )
        contact_info7 = ContactInformation.objects.create(
            postalCode='8000',
            street='Calle Urquiza',
            streetNumber='404',
            city='Mar del Plata',
            province='Buenos Aires'
        )
        contact_info8 = ContactInformation.objects.create(
            postalCode='9000',
            street='Calle Moreno',
            streetNumber='505',
            city='Comodoro Rivadavia',
            province='Chubut'
        )
        contact_info10 = ContactInformation.objects.create(
            postalCode='5100',
            street='Calle Alguna',
            streetNumber='348',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info11 = ContactInformation.objects.create(
            postalCode='5110',
            street='Calle Nose',
            streetNumber='857',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info12 = ContactInformation.objects.create(
            postalCode='5111',
            street='Calle Nose2',
            streetNumber='867',
            city='Córdoba',
            province='Córdoba'
        )
        contact_info13 = ContactInformation.objects.create(
            postalCode='8002',
            street='Calle Urna',
            streetNumber='405',
            city='Mar del Plata',
            province='Buenos Aires'
        )
        contact_info14 = ContactInformation.objects.create(
            postalCode='5020',
            street='Calle Las Heras',
            streetNumber='512',
            city='Córdoba',
            province='Córdoba'
        )

        contact_info15 = ContactInformation.objects.create(
            postalCode='5030',
            street='Avenida Illia',
            streetNumber='620',
            city='Córdoba',
            province='Córdoba'
        )

        # Crear escuela
        school = School.objects.create(
            name='Jesús María',
            abbreviation='JM',
            logo= logojesusmaria,
            email='contacto@jesusmaria.edu',
            contactInfo=contact_info14
            
        )
        school2 = School.objects.create(
            name='Villada',
            abbreviation='ITS.V',
            logo= logoits,
            email='contacto@its.edu',
            contactInfo=contact_info15
            
        )

      

        # Crear usuarios personalizados para la escuela "Jesús María"
        teacherJM = []
        directive_user = CustomUser.objects.create_user(
            email='directive@jesusmaria.edu',
            password='password',
            first_name='Carlos',
            last_name='Pérez',
            gender='masculino',  
            document='12345678',
            profile_picture= photoDirectiveJM,
            hoursToWork=40,
            phone='3516472286',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info1,
            email_verified=True,
            dark_mode=True
        )
        teacherJM.append(directive_user)

        teacher1 = CustomUser.objects.create_user(
            email='teacher1@jesusmaria.edu',
            password='password',
            first_name='María',
            last_name='González',
            gender='femenino',  
            document='87654321',
            profile_picture= photoTeacherJM,
            hoursToWork=30,
            phone='3516482287',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info2,
            email_verified=True
        )
        teacherJM.append(teacher1)

        teacher2 = CustomUser.objects.create_user(
            email='teacher2@jesusmaria.edu',
            password='password',
            first_name='José',
            last_name='Martínez',
            gender='masculino',  
            document='11223344',
            profile_picture= defaultuser,
            hoursToWork=35,
            phone='3516492288',  
            documentType=passport,
            nationality=uruguay,
            contactInfo=contact_info3
        )
        teacherJM.append(teacher2)

        teacher3 = CustomUser.objects.create_user(
            email='teacher3@jesusmaria.edu',
            password='password',
            first_name='Laura',
            last_name='Fernández',
            gender='femenino',  
            document='22334455',
            profile_picture= defaultuser,
            hoursToWork=32,
            phone='3516502289',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info4
        )
        teacherJM.append(teacher3)

        teacher4 = CustomUser.objects.create_user(
            email='teacher4@jesmaria.edu',
            password='password',
            first_name='Ricardo',
            last_name='García',
            gender='masculino',  
            document='33445566',
            profile_picture= defaultuser,
            hoursToWork=40,
            phone='3516512290',  
            documentType=dni,
            nationality=brasil,
            contactInfo=contact_info5
        )
        teacherJM.append(teacher4)

        teacher5 = CustomUser.objects.create_user(
            email='teacher5@jesmaria.edu',
            password='password',
            first_name='Ana',
            last_name='Rodríguez',
            gender='femenino',  
            document='44556677',
            profile_picture= defaultuser,
            hoursToWork=28,
            phone='3516522291',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info6
        )
        teacherJM.append(teacher5)

        preceptor1 = CustomUser.objects.create_user(
            email='preceptor1@jesmaria.edu',
            password='password',
            first_name='David',
            last_name='López',
            gender='masculino',  
            document='55667788',
            profile_picture= defaultuser,
            hoursToWork=20,
            phone='3516532292',  
            documentType=dni,
            nationality=chile,
            contactInfo=contact_info7
        )

        preceptor2 = CustomUser.objects.create_user(
            email='preceptor2@jesmaria.edu',
            password='password',
            first_name='Elena',
            last_name='Torres',
            gender='femenino',  
            document='66778899',
            profile_picture= defaultuser,
            hoursToWork=25,
            phone='3516542293',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info8
        )

        # Usuarios de la escuela Villada

        teacherV = []
        directive_user2 = CustomUser.objects.create_user(
            email='directive@villada.edu',
            password='password',
            first_name='Monica',
            last_name='Flores',
            gender='femenino',  
            document='12345679',
            profile_picture= photoDirectiveVillada,
            hoursToWork=40,
            phone='3516552294',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info10,
            email_verified=True,
            dark_mode=True
        )

        teacher1_2 = CustomUser.objects.create_user(
            email='teacher1_2@villada.edu',
            password='password',
            first_name='Mario',
            last_name='González',
            gender='masculino',  
            document='87654326',
            profile_picture= defaultuser,
            hoursToWork=30,
            phone='3516562295',  
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info11,
            email_verified=True
        )
        teacherV.append(teacher1_2)

        teacher2_2 = CustomUser.objects.create_user(
            email='teacher2_2@villada.edu',
            password='password',
            first_name='Josefina',
            last_name='Martinolli',
            gender='femenino',  
            document='11223324',
            profile_picture= defaultuser,
            hoursToWork=35,
            phone='3516572296',  
            documentType=passport,
            nationality=uruguay,
            contactInfo=contact_info12
        )
        teacherV.append(teacher2_2)

        preceptor1_2 = CustomUser.objects.create_user(
            email='preceptor1_2@villada.edu',
            password='password',
            first_name='Derek',
            last_name='López',
            gender='masculino',  
            document='55617788',
            profile_picture= defaultuser,
            hoursToWork=20,
            phone='3516582297',  
            documentType=passport,
            nationality=bolivia,
            contactInfo=contact_info13
        )



        # Asignar directivos a la escuela
        school.directives.add(directive_user)
        school2.directives.add(directive_user2)

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
        modulesV = []
        for i, day in enumerate(days_of_week, start=1):
            for j in range(1, 6):
                module = Module.objects.create(
                    moduleNumber=j,
                    day=day,
                    startTime=time(8 + j, 0),
                    endTime=time(9 + j, 0),
                    school=school2
                )
                modulesV.append(module)

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

        # Crear disponibilidad de profesor en Villada
        for j, teacher in enumerate(teacherV):
            for i, module in enumerate(modulesV):
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

        year1.preceptors.add(directive_user)
        year2.preceptors.add(preceptor1)
        year3.preceptors.add(preceptor1)
        year4.preceptors.add(preceptor2)
        year5.preceptors.add(preceptor2)
        year6.preceptors.add(preceptor2)

        # Crear años Villada

        year1_2 = Year.objects.create(name='1er Año', number='1', school=school2)
        year2_2 = Year.objects.create(name='2do Año', number='2', school=school2)
        year3_2 = Year.objects.create(name='3er Año', number='3', school=school2)
        year4_2 = Year.objects.create(name='4to Año', number='4', school=school2)
        year5_2 = Year.objects.create(name='5to Año', number='5', school=school2)
        year6_2 = Year.objects.create(name='6to Año', number='6', school=school2)
        year7_2 = Year.objects.create(name='7mo Año', number='7', school=school2)

        year1_2.preceptors.add(preceptor1_2)
        year2_2.preceptors.add(preceptor1_2)
        year3_2.preceptors.add(preceptor1_2)
        year4_2.preceptors.add(preceptor1_2)
        year5_2.preceptors.add(preceptor1_2)
        year6_2.preceptors.add(preceptor1_2)
        year7_2.preceptors.add(preceptor1_2)

        # Crear Curso
        course_names = ['A', 'B', 'C']

        # Crear cursos para los años de Jesús María
        coursesJM = []
        for year in [year1, year2, year3, year4, year5, year6]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                coursesJM.append(course)

        # Crear cursos para los años de Villada
        coursesV = []
        for year in [year1_2, year2_2, year3_2, year4_2, year5_2, year6_2, year7_2]:
            for name in course_names:
                course_name = f"{year.number}°{name}"
                course = Course.objects.create(name=course_name, year=year)
                coursesV.append(course)


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
            name="Fisica",
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

        # Crear materias Villada
        subjectsV = []

        subject1_2 = Subject.objects.create(
            name="Lengua",
            color='#E74C3C',  
            abbreviation="LEN",
            school=school2
        )
        subjectsV.append(subject1_2)

        subject2_2 = Subject.objects.create(
            name="Filosofía",
            color='#16A085',  
            abbreviation="FIL",
            school=school2
        )
        subjectsV.append(subject2_2)

        subject3_2 = Subject.objects.create(
            name="Historia",
            color='#D35400',  
            abbreviation="HIS",
            school=school2
        )
        subjectsV.append(subject3_2)

        subject4_2 = Subject.objects.create(
            name="Programación",
            color='#3498DB',  
            abbreviation="PROG",
            school=school2
        )
        subjectsV.append(subject4_2)


        # Asignar materias a cursos
        coursesubjectJM = []
        for j, subject in enumerate(subjectsJM):
            for i, course in enumerate(coursesJM):
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(studyPlan=studyPlan, subject=subject, course=course, weeklyHours=5)
                coursesubjectJM.append(coursesubject)
        print(len(coursesubjectJM))
        coursesubjectV = []
        for j, subject in enumerate(subjectsV):
            for i, course in enumerate(coursesV):
                studyPlan = f"Plan de estudio de {subject.name} {course.name}"
                coursesubject = CourseSubjects.objects.create(studyPlan=studyPlan, subject=subject, course=course, weeklyHours=5)
                coursesubjectV.append(coursesubject)
        print(len(coursesubjectV))


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

        # TSS Villada
        for i, coursesubject in enumerate(coursesubjectV):
            print(coursesubject)
            # Determinar el profesor actual usando división entera
            teacher = teacherV[(i // subjects_per_teacher) % len(teacherV)]
            TeacherSubjectSchool.objects.create(
                school=school2,
                coursesubjects=coursesubject,
                teacher=teacher
            )
        TeacherSubjectSchool.objects.create(school=school2, coursesubjects=coursesubjectV[3], teacher=directive_user)

        
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
            endDate=timezone.now() + timedelta(days=1, hours=2),
            school=school,
            eventType=event_type1
        )
        event1.roles.add(teacher_role)
        event1.affiliated_teachers.add(teacher1, teacher4)


        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))