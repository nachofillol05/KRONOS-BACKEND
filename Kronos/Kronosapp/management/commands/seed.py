from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event, Role, CourseSubjects
)
import uuid
from django.utils import timezone
from datetime import time, timedelta
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

        # Crear información de contacto

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
        contact_info9 = ContactInformation.objects.create(
            postalCode='9100',
            street='Calle Morena',
            streetNumber='506',
            city='Comodoro Rivadavio',
            province='Cordoba'
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

        # Crear escuela
        school = School.objects.create(
            name='Jesús María',
            abbreviation='JM',
            email='contacto@jesusmaria.edu',
            contactInfo=contact_info1
        )
        school2 = School.objects.create(
            name='Villada',
            abbreviation='ITS.V',
            email='contacto@its.edu',
            contactInfo=contact_info9
        )

        # Crear usuarios personalizados para escuela 1(directivos, profesores, preceptores)
        
        directive_user = CustomUser.objects.create_user(
            email='directive@jesusmaria.edu',
            password='password',
            first_name='Carlos',
            last_name='Pérez',
            gender='male',
            document='12345678',
            hoursToWork=40,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info1,
            email_verified=True,
            dark_mode=True
        )
        
        teacher1 = CustomUser.objects.create_user(
            email='teacher1@jesusmaria.edu',
            password='password',
            first_name='María',
            last_name='González',
            gender='female',
            document='87654321',
            hoursToWork=30,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info2,
            email_verified=True
        )
        teacher2 = CustomUser.objects.create_user(
            email='teacher2@jesusmaria.edu',
            password='password',
            first_name='José',
            last_name='Martínez',
            gender='male',
            document='11223344',
            hoursToWork=35,
            documentType=passport,
            nationality=uruguay,
            contactInfo=contact_info3
        )
        teacher3 = CustomUser.objects.create_user(
            email='teacher3@jesusmaria.edu',
            password='password',
            first_name='Laura',
            last_name='Fernández',
            gender='female',
            document='22334455',
            hoursToWork=32,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info4
        )
        teacher4 = CustomUser.objects.create_user(
            email='teacher4@jesusmaria.edu',
            password='password',
            first_name='Ricardo',
            last_name='García',
            gender='male',
            document='33445566',
            hoursToWork=40,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info5
        )
        teacher5 = CustomUser.objects.create_user(
            email='teacher5@jesusmaria.edu',
            password='password',
            first_name='Ana',
            last_name='Rodríguez',
            gender='female',
            document='44556677',
            hoursToWork=28,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info6
        )
        preceptor1 = CustomUser.objects.create_user(
            email='preceptor1@jesusmaria.edu',
            password='password',
            first_name='David',
            last_name='López',
            gender='male',
            document='55667788',
            hoursToWork=20,
            documentType=passport,
            nationality=uruguay,
            contactInfo=contact_info7
        )
        preceptor2 = CustomUser.objects.create_user(
            email='preceptor2@jesusmaria.edu',
            password='password',
            first_name='Elena',
            last_name='Torres',
            gender='female',
            document='66778899',
            hoursToWork=25,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info8
        )

        # Crear usuarios personalizados para escuela 2(directivos, profesores, preceptores)

        directive_user2 = CustomUser.objects.create_user(
            email='directive@villada.edu',
            password='password',
            first_name='Monica',
            last_name='Flores',
            gender='male',
            document='12345679',
            hoursToWork=40,
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
            last_name='Gonzonalez',
            gender='male',
            document='87654326',
            hoursToWork=30,
            documentType=dni,
            nationality=argentina,
            contactInfo=contact_info11,
            email_verified=True
        )
        teacher2_2 = CustomUser.objects.create_user(
            email='teacher2_2@villada.edu',
            password='password',
            first_name='Josefina',
            last_name='Martinolli',
            gender='female',
            document='11223324',
            hoursToWork=35,
            documentType=passport,
            nationality=uruguay,
            contactInfo=contact_info12
        )
        preceptor1_2 = CustomUser.objects.create_user(
            email='preceptor1_2@villada.edu',
            password='password',
            first_name='Derek',
            last_name='López',
            gender='male',
            document='55617788',
            hoursToWork=20,
            documentType=passport,
            nationality=uruguay,
            contactInfo=contact_info13
        )

        # Asignar directivos a la escuela
        school.directives.add(directive_user)
        school2.directives.add(directive_user2)

        # Crear módulos
        days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']
        modules = []
        for i, day in enumerate(days_of_week, start=1):
            for j in range(1, 6):
                module = Module.objects.create(
                    moduleNumber=j,
                    day=day,
                    startTime=time(8 + j, 0),
                    endTime=time(9 + j, 0),
                    school=school
                )
                modules.append(module)

        # Crear estados de disponibilidad
        available = AvailabilityState.objects.create(name='Disponible', isEnabled=True)
        not_available = AvailabilityState.objects.create(name='No Disponible', isEnabled=False)

        # Crear disponibilidad de profesor
        for i, module in enumerate(modules):
            TeacherAvailability.objects.create(
                module=module,
                teacher=teacher1 if i % 2 == 0 else teacher2,
                availabilityState=available if i % 2 == 0 else not_available
            )

        # Crear años, cursos y materias
        year1 = Year.objects.create(name='1er Año', number='1', school=school)
        year2 = Year.objects.create(name='2do Año', number='2', school=school)

        year1.preceptors.add(preceptor1)
        year2.preceptors.add(preceptor2)

        year1_2 = Year.objects.create(name='1er Año', number='1', school=school2)
        year2_2 = Year.objects.create(name='2do Año', number='2', school=school2)

        year1_2.preceptors.add(preceptor1_2)


        # Crear cursos

        course1 = Course.objects.create(name='1°A', year=year1)
        course2 = Course.objects.create(name='1°B', year=year1)
        course3 = Course.objects.create(name='1°C', year=year1)
        course4 = Course.objects.create(name='2°A', year=year2)
        course5 = Course.objects.create(name='2°B', year=year2)
        course6 = Course.objects.create(name='2°C', year=year2)

        course1_2 = Course.objects.create(name='1°A', year=year1_2)
        course2_2 = Course.objects.create(name='1°B', year=year1_2)
        course3_2 = Course.objects.create(name='1°C', year=year1_2)
        course4_2 = Course.objects.create(name='2°A', year=year2_2)
        course5_2 = Course.objects.create(name='2°B', year=year2_2)
        course6_2 = Course.objects.create(name='2°C', year=year2_2)


        # Crear materias
        subject1 = Subject.objects.create(
            name="Matemáticas",
            abbreviation="MAT"
        )

        subject2 = Subject.objects.create(
            name="Fisica",
            abbreviation="FIS"
        )

        subject3 = Subject.objects.create(
            name="Química",
            abbreviation="QUI"
        )

        subject1_2 = Subject.objects.create(
            name="Lengua",
            abbreviation="Len"
        )

        subject2_2 = Subject.objects.create(
            name="Filosofía",
            abbreviation="FIL"
        )

        subject3_2 = Subject.objects.create(
            name="Historia",
            abbreviation="HIS"
        )

        # Asignar materias a cursos
        course_subject = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Matemáticas 1",
            subject=subject1,
            course=course1,
            weeklyHours=4
        )

        course_subject2 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Matemáticas 2",
            subject=subject1,
            course=course2,
            weeklyHours=4
        )

        course_subject3 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Matemáticas 3",
            subject=subject1,
            course=course3,
            weeklyHours=4
        )

        course_subject4 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Matemáticas 4",
            subject=subject1,
            course=course4,
            weeklyHours=3
        )

        course_subject5 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Fisica",
            subject=subject2,
            course=course2,
            weeklyHours=4
        )

        course_subject6 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Química",
            subject=subject3,
            course=course3,
            weeklyHours=4
        )

        course_subject_2 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Lengua 1",
            subject=subject1_2,
            course=course1_2,
            weeklyHours=4
        )

        course_subject2_2 = CourseSubjects.objects.create(
            studyPlan="Plan de estudios de Filosofia 2",
            subject=subject2_2,
            course=course2_2,
            weeklyHours=4
        )

        # Asignar profesor a materia en una escuela
        TeacherSubjectSchool.objects.create(
            school=school,
            coursesubjects=course_subject,
            teacher=teacher1
        )

        TeacherSubjectSchool.objects.create(
            school=school,
            coursesubjects=course_subject2,
            teacher=teacher1
        )

        TeacherSubjectSchool.objects.create(
            school=school,
            coursesubjects=course_subject3,
            teacher=teacher1
        )

        TeacherSubjectSchool.objects.create(
            school=school,
            coursesubjects=course_subject5,
            teacher=teacher2
        )

        TeacherSubjectSchool.objects.create(
            school=school,
            coursesubjects=course_subject6,
            teacher=teacher3
        )

        TeacherSubjectSchool.objects.create(
            school=school2,
            coursesubjects=course_subject_2,
            teacher=teacher1_2
        )

        TeacherSubjectSchool.objects.create(
            school=school2,
            coursesubjects=course_subject2_2,
            teacher=directive_user2
        )
        # Crear acciones
        action1 = Action.objects.create(name='Agregar materia', isEnabled=True)
        action2 = Action.objects.create(name='Cambiar materia', isEnabled=False)


        # Crear tipos de eventos
        event_type1 = EventType.objects.create(name='Paro de transporte', description='Interrupción de servicios de transporte')
        event_type2 = EventType.objects.create(name='Viaje escolar', description='Excursión organizada por la escuela')

        # Crear roles
        directive_role = Role.objects.create(name='Directive')
        teacher_role = Role.objects.create(name='Teacher')
        preceptor_role = Role.objects.create(name='Preceptor')

        # Crear evento
        event1 = Event.objects.create(
            name='Paro general de transporte',
            startDate=timezone.now() + timedelta(days=5),
            endDate=timezone.now() + timedelta(days=5, hours=2),
            school=school,
            eventType=event_type1
        )
        event1.roles.add(directive_role)
        event1.affiliated_teachers.add(teacher3, teacher4)


        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))