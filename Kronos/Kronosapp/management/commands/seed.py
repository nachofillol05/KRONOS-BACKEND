from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event, CourseSubjects
)
import uuid
from django.utils import timezone
from datetime import time, timedelta

class Command(BaseCommand):
    help = 'Seed database with initial data'
    # python manage.py seed
    def handle(self, *args, **options):
        # Crear tipos de documentos
        doc_type1 = DocumentType.objects.create(name='DNI', description='Documento Nacional de Identidad')
        doc_type2 = DocumentType.objects.create(name='Pasaporte', description='Documento de viaje internacional')

        # Crear nacionalidades
        nationality1 = Nationality.objects.create(name='Argentina', description='Nacionalidad argentina')
        nationality2 = Nationality.objects.create(name='Uruguay', description='Nacionalidad uruguaya')

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

        # Crear usuarios personalizados
        directive_user = CustomUser.objects.create_user(
            email='directive@jesusmaria.edu',
            password='password',
            first_name='Carlos',
            last_name='Pérez',
            gender='male',
            document='12345678',
            hoursToWork=40,
            documentType=doc_type1,
            nationality=nationality1,
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
            documentType=doc_type2,
            nationality=nationality2,
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
            documentType=doc_type1,
            nationality=nationality1,
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
            documentType=doc_type2,
            nationality=nationality2,
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
            documentType=doc_type1,
            nationality=nationality1,
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
            documentType=doc_type2,
            nationality=nationality2,
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
            documentType=doc_type1,
            nationality=nationality1,
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
            documentType=doc_type2,
            nationality=nationality2,
            contactInfo=contact_info8
        )

        # Crear escuela
        school1 = School.objects.create(
            name='Jesús María',
            abbreviation='JM',
            email='contacto@jesusmaria.edu',
            contactInfo=contact_info1
        )
        school1.directives.add(directive_user)

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
                    school=school1
                )
                modules.append(module)

        # Crear estados de disponibilidad
        available = AvailabilityState.objects.create(name='Disponible', isEnabled=True)
        not_available = AvailabilityState.objects.create(name='No Disponible', isEnabled=False)

        # Crear disponibilidad del profesor
        for i, module in enumerate(modules):
            TeacherAvailability.objects.create(
                module=module,
                teacher=teacher1 if i % 2 == 0 else teacher2,
                availabilityState=available if i % 2 == 0 else not_available
            )

        # Crear años, cursos y materias
        year1 = Year.objects.create(name='1er Año', number='1', school=school1)
        year2 = Year.objects.create(name='2do Año', number='2', school=school1)

        year1.preceptors.add(preceptor1)
        year2.preceptors.add(preceptor2)

        course1 = Course.objects.create(name='1°A', year=year1)
        course2 = Course.objects.create(name='1°B', year=year1)
        course3 = Course.objects.create(name='1°C', year=year1)
        course4 = Course.objects.create(name='2°A', year=year2)
        course5 = Course.objects.create(name='2°B', year=year2)
        course6 = Course.objects.create(name='2°C', year=year2)

        subject1 = Subject.objects.create(
            name='Matematica',
            abbreviation='mat', 
            weeklyHours=4,
            school=course1,
            studyPlan='Plan de estudios de geografía'
        )
        subject2 = Subject.objects.create(
            name='Matematica',
            abbreviation='mat',
            weeklyHours=4,
            school=course2
        )
        subject3 = Subject.objects.create(
            name='Matematica',
            abbreviation='mat',
            weeklyHours=4,
            school=course3
        )
        subject4 = Subject.objects.create(
            name='Lengua',
            abbreviation='len',
            weeklyHours=3,
            school=course4
        )
        subject5 = Subject.objects.create(
            name='Lengua',
            abbreviation='len',
            weeklyHours=3,
            school=course5
        )
        subject6 = Subject.objects.create(
            name='Lengua',
            abbreviation='len',
            weeklyHours=3,
            school=course6
        )
        subject7 = Subject.objects.create(
            name='Historia Mundial',
            abbreviation='his',
            weeklyHours=2,
            school=course1
        )
        subject8 = Subject.objects.create(
            name='Historia Mundial',
            abbreviation='his',
            weeklyHours=2,
            school=course2
        )
        subject9 = Subject.objects.create(
            name='Historia Mundial',
            abbreviation='his',
            weeklyHours=2,
            school=course3
        )
        subject10 = Subject.objects.create(
            name='Geografía',
            abbreviation='geo',
            weeklyHours=2,
            school=course4
        )
        subject11 = Subject.objects.create(
            name='Geografía',
            abbreviation='geo',
            weeklyHours=2,
            school=course5
        )
        subject12 = Subject.objects.create(
            name='Geografía',
            abbreviation='geo',
            weeklyHours=2,
            school=course6
        )

        cs1 = CourseSubjects.objects.create(subject=subject12, course=course3)
        cs2 = CourseSubjects.objects.create(subject=subject11, course=course2, studyPlan='Plan de estudios de geografía')
        cs3 = CourseSubjects.objects.create(subject=subject10, course=course1, studyPlan='Plan de estudios de historia mundial')
        cs4 = CourseSubjects.objects.create(subject=subject9, course=course3, studyPlan='Plan de estudios de historia mundial')
        cs5 = CourseSubjects.objects.create(subject=subject8, course=course2, studyPlan='Plan de estudios de historia mundial')
        cs6 = CourseSubjects.objects.create(subject=subject7, course=course1, studyPlan='Plan de estudios de Lengua')
        cs7 = CourseSubjects.objects.create(subject=subject6, course=course3, studyPlan='Plan de estudios de Lengua')
        cs8 = CourseSubjects.objects.create(subject=subject5, course=course2, studyPlan='Plan de estudios de Lengua')
        cs9 = CourseSubjects.objects.create(subject=subject4, course=course1, studyPlan='Plan de estudios de Matematica')
        cs10 = CourseSubjects.objects.create(subject=subject3, course=course3, studyPlan='Plan de estudios de Matematica')
        cs11= CourseSubjects.objects.create(subject=subject2, course=course2, studyPlan='Plan de estudios de Matematica')
        cs12 = CourseSubjects.objects.create(subject=subject1, course=course1, studyPlan='Plan de estudios de Matematica')

        


        # Teacher Subject School
        TeacherSubjectSchool.objects.create(school=school1, subject=cs1, teacher=teacher1)
        TeacherSubjectSchool.objects.create(school=school1, subject=cs2, teacher=teacher2)
        TeacherSubjectSchool.objects.create(school=school1, subject=cs3, teacher=teacher3)
        TeacherSubjectSchool.objects.create(school=school1, subject=cs4, teacher=teacher4)

        # Crear acciones
        action1 = Action.objects.create(name='Agregar materia', isEnabled=True)
        action2 = Action.objects.create(name='Cambiar materia', isEnabled=False)


        # Crear tipo de evento
        event_type1 = EventType.objects.create(name='Paro de transporte', description='Interrupción de servicios de transporte')
        event_type2 = EventType.objects.create(name='Viaje escolar', description='Excursión organizada por la escuela')


        # Crear evento
        event1 = Event.objects.create(
            name='Paro general de transporte',
            startDate=timezone.now() + timedelta(days=5),
            endDate=timezone.now() + timedelta(days=5, hours=2),
            school=school1,
            eventType=event_type1
        )
        event2 = Event.objects.create(
            name='Viaje a museo',
            startDate=timezone.now() + timedelta(days=15),
            endDate=timezone.now() + timedelta(days=15, hours=8),
            school=school1,
            eventType=event_type2
        )
        event3 = Event.objects.create(
            name='Visita a la universidad',
            startDate=timezone.now() + timedelta(days=30),
            endDate=timezone.now() + timedelta(days=30, hours=6),
            school=school1,
            eventType=event_type2
        )

        # Asignar profesores a los eventos
        event1.affiliated_teachers.add(teacher1)
        event2.affiliated_teachers.add(teacher2)
        event3.affiliated_teachers.add(teacher3, teacher4)



        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))