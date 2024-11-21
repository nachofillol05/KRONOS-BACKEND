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
