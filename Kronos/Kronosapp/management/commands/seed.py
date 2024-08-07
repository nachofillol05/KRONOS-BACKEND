from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event
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
            username='directive',
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
            username='teacher1',
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
            username='teacher2',
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
            username='teacher3',
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
            username='teacher4',
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
            username='teacher5',
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
            username='preceptor1',
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
            username='preceptor2',
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
            studyPlan='Plan de estudios de Matematica',
            weeklyHours=4,
            course=course1
        )
        subject2 = Subject.objects.create(
            name='Matematica',
            abbreviation='mat',
            studyPlan='Plan de estudios de Matematica',
            weeklyHours=4,
            course=course2
        )
        subject3 = Subject.objects.create(
            name='Matematica',
            abbreviation='mat',
            studyPlan='Plan de estudios de Matematica',
            weeklyHours=4,
            course=course3
        )
        subject4 = Subject.objects.create(
            name='Lengua',
            abbreviation='len',
            studyPlan='Plan de estudios de Lengua',
            weeklyHours=3,
            course=course1
        )
        subject5 = Subject.objects.create(
            name='Lengua',
            abbreviation='len',
            studyPlan='Plan de estudios de Lengua',
            weeklyHours=3,
            course=course2
        )
        subject6 = Subject.objects.create(
            name='Lengua',
            abbreviation='len',
            studyPlan='Plan de estudios de Lengua',
            weeklyHours=3,
            course=course3
        )
        subject7 = Subject.objects.create(
            name='Historia Mundial',
            abbreviation='his',
            studyPlan='Plan de estudios de historia mundial',
            weeklyHours=2,
            course=course1
        )
        subject8 = Subject.objects.create(
            name='Historia Mundial',
            abbreviation='his',
            studyPlan='Plan de estudios de historia mundial',
            weeklyHours=2,
            course=course2
        )
        subject9 = Subject.objects.create(
            name='Historia Mundial',
            abbreviation='his',
            studyPlan='Plan de estudios de historia mundial',
            weeklyHours=2,
            course=course3
        )
        subject10 = Subject.objects.create(
            name='Geografía',
            abbreviation='geo',
            studyPlan='Plan de estudios de geografía',
            weeklyHours=2,
            course=course1
        )
        subject11 = Subject.objects.create(
            name='Geografía',
            abbreviation='geo',
            studyPlan='Plan de estudios de geografía',
            weeklyHours=2,
            course=course2
        )
        subject12 = Subject.objects.create(
            name='Geografía',
            abbreviation='geo',
            studyPlan='Plan de estudios de geografía',
            weeklyHours=2,
            course=course3
        )

        # Teacher Subject School
        TeacherSubjectSchool.objects.create(school=school1, subject=subject1, teacher=teacher1)
        TeacherSubjectSchool.objects.create(school=school1, subject=subject2, teacher=teacher2)
        TeacherSubjectSchool.objects.create(school=school1, subject=subject3, teacher=teacher3)
        TeacherSubjectSchool.objects.create(school=school1, subject=subject4, teacher=teacher4)

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