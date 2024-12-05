from ..models import(
    CustomUser,
    TeacherSubjectSchool,
    Subject,
    Module,
    Course,
    Schedules,
    Action,
    CourseSubjects,
    TeacherAvailability,
    Course,
    AvailabilityState,
)
from django.core.cache import cache
from django.db import connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from ..permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime
from ..schedule_creation import schedule_creation
from ..serializers.Subject_serializer import SubjectWithCoursesSerializer
from ..serializers.schedule_serializer import ScheduleSerializer, CreateScheduleSerializer
from ..serializers.history_serializer import HistorySerializer
from ..utils import call_free_teacher,call_free_subject, change_teacher_aviability
from datetime import datetime
from django.db.models import F, Window, Value, Q
from django.db.models.functions import Rank, Concat
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models import Schedules, Module, TeacherSubjectSchool, CourseSubjects, CustomUser, Subject, Course
from ..utils import convert_binary_to_image
from ..permissions import SchoolHeader, IsDirectiveOrOnlyRead


class CreateModuleSchedule(generics.CreateAPIView):
    """
    Crear un modulo de horario
    """
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializer_class = CreateScheduleSerializer

    def get_serializer_class(self):
        self.request.data['date'] = datetime.now().isoformat()
        return CreateScheduleSerializer


class Newscheduleview(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request, *args, **kwargs):
        result = schedule_creation(user_school=self.request.school)
        modules = result[0]
        cache.set('schedule_result', modules, timeout=3600)  # Guardar por 1 hora
        return Response(result)
    

class NewScheduleCreation(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def post(self, request):
        results = cache.get('schedule_result')
        if results is None:
            return Response({'error': 'Schedule not found'}, status=404)
        else: 
            for module in results:
                day = module['day']
                hour = module['moduleNumber']
                tss_id = module['tss_id']
                school_id = module['school_id']

                try:
                    module = Module.objects.get(day=day, moduleNumber=hour, school=school_id)
                except Module.DoesNotExist:
                    return Response({'error': f'Module for day {day} and hour {hour} not found'}, status=404)
                try:
                    tss = TeacherSubjectSchool.objects.get(id=tss_id)
                except Module.DoesNotExist:
                    return Response({'error': f'Teacher not found'}, status=404)

                try:
                    action = Action.objects.get(name="agregar materia con automatizacion")
                except Action.DoesNotExist:
                    action = Action.objects.create(name="agregar materia con automatizacion")

                newschedule = Schedules(date=datetime.now(), action=action, module=module, tssId=tss)
                newschedule.save()
                change_teacher_aviability(module, tss.teacher)

            return Response({'message': 'Schedules created successfully'})  


class ViewSchedule(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializer_class = ScheduleSerializer

    def get(self, request):
        date = self.request.query_params.get('date', None)
        teachers = self.request.query_params.getlist('teachers', None)
        courses = self.request.query_params.getlist('courses', None)

        # Validar teachers
        if teachers:
            try:
                teacher_ids = [int(teacher) for teacher in teachers]
                for teacher_id in teacher_ids:
                    if not CustomUser.objects.filter(pk=teacher_id).exists():
                        raise ValidationError({'error': '"teachers_ids": no válido.'})
            except ValueError:
                raise ValidationError("Los teachers proporcionados no existen.")
        else:
            teacher_ids = None

        # Validar courses
        if courses:
            try:
                course_ids = [int(course) for course in courses]
                for course_id in course_ids:
                    if not Course.objects.filter(pk=course_id).exists():
                        raise ValidationError({'error': '"courses_ids": no válido.'})
            except ValueError:
                raise ValidationError("Los courses proporcionados no existen.")
        else:
            course_ids = None

        # Validar y formatear la fecha
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        # Usar el ORM para replicar la lógica de la consulta SQL
        schedules = Schedules.objects.filter(
            date__lte=date
        ).annotate(
            rank=Window(
                expression=Rank(),
                partition_by=[F('module_id'), F('tssId__coursesubjects__course_id')],
                order_by=F('date').desc()
            ),
            teacher_id=F('tssId__teacher_id'),
            course_id=F('tssId__coursesubjects__course_id'),
            subject_id=F('tssId__coursesubjects__subject_id'),
            course_name=F('tssId__coursesubjects__course__name'),
            day=F('module__day'),
            module_number=F('module__moduleNumber'),
            subject_name=F('tssId__coursesubjects__subject__name'),
            subject_abbreviation=F('tssId__coursesubjects__subject__abbreviation'),
            subject_color=F('tssId__coursesubjects__subject__color'),
            nombre=Concat(F('tssId__teacher__first_name'), Value(' '), F('tssId__teacher__last_name')),
            profile_picture=F('tssId__teacher__profile_picture'),
        ).filter(rank=1).order_by('course_id', 'module_id')

        # Filtrar por teacher_ids y course_ids si existen
        if teacher_ids:
            schedules = schedules.filter(teacher_id__in=teacher_ids)
        if course_ids:
            schedules = schedules.filter(course_id__in=course_ids)

        # Construir la respuesta final
        data = []
        for schedule in schedules:
            if schedule.subject_name != "freeSubject":
                data.append({
                    "id": schedule.id,
                    "date": schedule.date,
                    "module_id": schedule.module_id,
                    "course_id": schedule.course_id,
                    "teacher_id": schedule.teacher_id,
                    "nombre": schedule.nombre,
                    "profile_picture": convert_binary_to_image(schedule.profile_picture) if schedule.profile_picture else None,
                    "subject_abreviation": schedule.subject_abbreviation,
                    "subject_color": schedule.subject_color,
                    "subject_id": schedule.subject_id,
                    "course_name": schedule.course_name,
                    "day": schedule.day,
                    "moduleNumber": schedule.module_number,
                    "subject_name": schedule.subject_name,
                })
        
        return Response(data)


class ViewHistorySchedule(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializer_class = HistorySerializer
    NAME_FREE_SUBJECT = "freeSubject"

    def get_queryset(self):
        school = self.request.school
        queryset = Schedules.objects.filter(module__school=school)
        queryset = queryset.exclude(tssId__coursesubjects__subject__name=self.NAME_FREE_SUBJECT)
        queryset = queryset.order_by('-date')
        return queryset


class ViewTeacherSchedule(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader]
    serializer_class = ScheduleSerializer

    def get(self, request):
        teacher_id = self.request.user.pk
        freeteacher = call_free_teacher()

        # Filtro base
        base_query = Schedules.objects.filter(
            Q(date__lte=datetime.now()) & 
            (Q(tssId__teacher_id=teacher_id) | Q(tssId__teacher_id=freeteacher))
        ).annotate(
            course_id=F("tssId__coursesubjects__course_id"),
            teacher_id=F("tssId__teacher_id"),
            subject_abreviation=F("tssId__coursesubjects__subject__abbreviation"),
            subject_color=F("tssId__coursesubjects__subject__color"),
            subject_id=F("tssId__coursesubjects__subject_id"),
            course_name=F("tssId__coursesubjects__course__name"),
            day=F("module__day"),
            moduleNumber=F("module__moduleNumber"),
            subject_name=F("tssId__coursesubjects__subject__name"),
            logo=F("tssId__school__logo"),
            school_name=F("tssId__school__name"),
            rank=Window(
                expression=Rank(),
                partition_by=[F("module_id"), F("tssId__coursesubjects__course_id")],
                order_by=F("date").desc(),
            )
        ).filter(rank=1, tssId__teacher_id=teacher_id).order_by("course_id", "module_id")

        # Construcción de los datos
        data = []
        for schedule in base_query:
            if schedule.subject_name != "freeSubject":
                data.append({
                    "id": schedule.id,
                    "date": schedule.date,
                    "module_id": schedule.module_id,
                    "course_id": schedule.course_id,
                    "teacher_id": schedule.teacher_id,
                    "subject_abreviation": schedule.subject_abreviation,
                    "subject_color": schedule.subject_color,
                    "subject_id": schedule.subject_id,
                    "course_name": schedule.course_name,
                    "day": schedule.day,
                    "moduleNumber": schedule.moduleNumber,
                    "subject_name": schedule.subject_name,
                    "logo": convert_binary_to_image(schedule.logo) if schedule.logo else None,
                    "school_name": schedule.school_name
                })

        if data:
            return Response(data)
        else:
            return Response(
                {'error': "No se encontraron materias para el profesor"},
                status=status.HTTP_404_NOT_FOUND
            )
            



class SubjectPerModuleView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializer_class = SubjectWithCoursesSerializer

    def get_queryset(self):
        module_id = self.request.query_params.get('module_id', None)
        course_id = self.request.query_params.get('course_id', None)

        if not module_id or not course_id:
            return Response(
                {'error': 'Se necesita pasar el ID del módulo y el ID del curso.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            module = Module.objects.get(id=module_id)
            course_subjects = CourseSubjects.objects.filter(course_id=course_id)
        except (Module.DoesNotExist, CourseSubjects.DoesNotExist):
            return Response(
                {'error': 'El módulo o el curso no existen.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        # VALIDACION CANTIDAD DE HORAS
        validate_course_subjects = []
        for course_subject in course_subjects:
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT COUNT(*)
                    FROM (
                        SELECT sh.id as id,
                            sh.date,
                            sh.module_id,
                            cs.id AS course_subject,
                            cs.course_id as course_id,
                            cs.subject_id,
                            RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                        FROM Kronosapp_schedules sh
                        INNER JOIN Kronosapp_module m 
                                ON sh.module_id = m.id
                        INNER JOIN Kronosapp_teachersubjectschool tss
                            ON sh.tssId_id = tss.id
                        INNER JOIN Kronosapp_coursesubjects cs
                            ON tss.coursesubjects_id = cs.id
                    ) as t
                    WHERE t.RN = 1
                    AND (t.course_subject = %s);
                    """
                cursor.execute(sql_query, [course_subject.id])
                weekly_hours_result = cursor.fetchone()
                
                if weekly_hours_result:
                    weeklyHours = int(weekly_hours_result[0])
                else:
                    weeklyHours = 0

            if weeklyHours < course_subject.weeklyHours:
                validate_course_subjects.append(course_subject)

        # VALIDACION PROFESOR DISPONIBLE
        available_coursesubjects = []
        for course_subject in validate_course_subjects:
            teacher_subject_school = TeacherSubjectSchool.objects.filter(coursesubjects=course_subject).first()
            if teacher_subject_school:
                teacher = teacher_subject_school.teacher
                if TeacherAvailability.objects.filter(teacher=teacher, module=module, availabilityState__isEnabled=True).exists():
                    available_coursesubjects.append(course_subject)

        # VALIDAR SI EL PROFESOR YA ESTA ASIGNADO EN ESE MODULO
        available_subjects = []
        for available_subject in available_coursesubjects:

            teacher_subject_school = TeacherSubjectSchool.objects.filter(coursesubjects=available_subject).first()

            #schedules_with_same_module = Schedules.objects.filter(module=module, tssId__school=self.request.school, tssId__teacher=teacher_subject_school.teacher)
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT *
                        FROM (
                            SELECT sh.id as id,
                                sh.date,
                                sh.module_id,
                                cs.course_id as course_id,
                                t.id as t_id,
                                RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                            FROM Kronosapp_schedules sh
                            INNER JOIN Kronosapp_module m 
                                    ON sh.module_id = m.id
                            INNER JOIN Kronosapp_teachersubjectschool tss
                                ON sh.tssId_id = tss.id
                            INNER JOIN Kronosapp_school sc
                                    ON tss.school_id = sc.id
                            INNER JOIN Kronosapp_coursesubjects cs
                                ON tss.coursesubjects_id = cs.id
                            INNER JOIN Kronosapp_customuser t
                                ON tss.teacher_id = t.id
                            INNER JOIN Kronosapp_subject s
                                ON cs.subject_id = s.id
                            INNER JOIN Kronosapp_course c 
                                    ON cs.course_id = c.id
                            WHERE DATE(sh.date) <=  %s
                            AND m.id = %s
                        ) as t
                        WHERE t.RN = 1
                        ORDER BY course_id, module_id;
                    """
                cursor.execute(sql_query, [datetime.now(), module.id])
                teachers_busy =  [row[4] for row in cursor.fetchall()]
            
            if teacher_subject_school.teacher.id not in teachers_busy:
                available_subjects.append(available_subject.subject)

        return Subject.objects.filter(id__in=[subject.id for subject in available_subjects])
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, Response):
            return queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        schedules_data = request.data.get('schedules', [])
        
        if not schedules_data:
            return Response({"error": "No se proporcionaron datos de horarios."}, status=status.HTTP_400_BAD_REQUEST)
        {
            "schedules": [{
                "course"
            }]
        }
        for schedule_data in schedules_data:
            
            course_id = schedule_data.get('course_id')
            module_id = schedule_data.get('module_id')
            subject_id = schedule_data.get('subject_id')
            
            if not course_id or not module_id or not subject_id:
                return Response({"error": "Se necesita pasar el ID del curso, el ID del módulo y el ID de materia."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                course_subject = CourseSubjects.objects.filter(course=course_id, subject=subject_id).first()
                
                teacher_subject_school = TeacherSubjectSchool.objects.get(coursesubjects=course_subject, school=request.school)
                module = Module.objects.get(id=module_id)
           
            except CourseSubjects.DoesNotExist:
                return Response({"error": "CourseSubject no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            except TeacherSubjectSchool.DoesNotExist:
                return Response({"error": "TeacherSubjectSchool no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            except Module.DoesNotExist:
                return Response({"error": "Módulo no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                action=Action.objects.get(name="agregar materia")
            except:
                action=Action.objects.create(name="agregar materia")

            schedule = Schedules.objects.create(
                date=datetime.now(),
                action=action,
                module=module,
                tssId=teacher_subject_school
            )

            
            teacher: CustomUser = schedule.tssId.teacher
            subject: Subject = schedule.tssId.coursesubjects.subject
            course: Course = schedule.tssId.coursesubjects.course
            module: Module = schedule.module
            from ..utils import convert_binary_to_image
            schedule_dict = {
                "id": schedule.pk,
                "date": schedule.date,
                "module_id": module.pk,
                "course_id": course.pk,
                "teacher_id": teacher.pk,
                "nombre": teacher.first_name + " " + teacher.last_name,
                "profile_picture": convert_binary_to_image(teacher.profile_picture) if teacher.profile_picture else None,
                "subject_abreviation": subject.abbreviation,
                "subject_color": subject.color,
                "subject_id": subject.pk,
                "course_name": course.name,
                "day": module.day,
                "moduleNumber": module.moduleNumber,
                "subject_name": subject.name
            }
            change_teacher_aviability(module, teacher_subject_school.teacher)

        return Response(schedule_dict, status=status.HTTP_201_CREATED)

    def delete(self, request):
        module_id = self.request.query_params.get('module_id', None)
        course_id = self.request.query_params.get('course_id', None)

        with connection.cursor() as cursor:
                sql_query = """
                    SELECT *
                        FROM (
                            SELECT sh.id as id,
                                sh.date,
                                sh.module_id,
                                cs.id AS course_subject,
                                cs.course_id as course_id,
                                tss.teacher_id AS teacher_id,
                                RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                            FROM Kronosapp_schedules sh
                            INNER JOIN Kronosapp_module m 
                                    ON sh.module_id = m.id
                            INNER JOIN Kronosapp_teachersubjectschool tss
                                ON sh.tssId_id = tss.id
                            INNER JOIN Kronosapp_coursesubjects cs
                                ON tss.coursesubjects_id = cs.id
                        ) as t
                        WHERE t.RN = 1
                        AND module_id = %s
                        AND course_id = %s;
                    """
                cursor.execute(sql_query, [module_id, course_id])
                results = cursor.fetchall()

                if not results:
                    return Response({'error': 'No se encontraron registros.'}, status=404)
                old_teacher = results[0][5]
                schedule_id = results[0][0]  
                teacher = int(old_teacher)
        
        if not module_id or not course_id:
            return Response({"error": "Se necesita pasar el ID del curso y el ID del módulo."}, status=status.HTTP_400_BAD_REQUEST)
        
        freesubject=call_free_subject(request.school)
        freeTeacher=call_free_teacher()
        try:
            module = Module.objects.get(pk=module_id)
        except Module.DoesNotExist:
            return Response({"error": "El modulo proporcionado no existe."}, status=status.HTTP_400_BAD_REQUEST)
        try: 
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "El curso proporcionado no existe."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course_subject = CourseSubjects.objects.get(course=course, subject=freesubject)
        except:
            course_subject = CourseSubjects.objects.create(course=course,subject=freesubject, weeklyHours=999, studyPlan= "")
        try:
            teacher_subject_school = TeacherSubjectSchool.objects.get(school=request.school, teacher=freeTeacher, coursesubjects=course_subject)
        except TeacherSubjectSchool.DoesNotExist:
            teacher_subject_school = TeacherSubjectSchool.objects.create(school=request.school, teacher=freeTeacher, coursesubjects=course_subject)
        
        
        try:
            state = Action.objects.get(name="eliminar materia")
        except Action.DoesNotExist:
            state = Action.objects.create(name="eliminar materia")
        schedule = Schedules.objects.get(id=schedule_id)
        schedule.action=state
        schedule.save()
        
        
        try:
            Schedules.objects.create(
                date = datetime.now(),
                action = None,
                module = module,
                tssId = teacher_subject_school
            )
        except:
            return Response({"error": "Error al eliminar el shedule."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if teacher:
            state = AvailabilityState.objects.get(name="Disponible")
            try:
                availability = TeacherAvailability.objects.get(teacher=teacher, module_id=module_id)
            except TeacherAvailability.DoesNotExist:
                return Response({"error": "No se encontro la disponibilidad del profesor."}, status=status.HTTP_404_NOT_FOUND)
            availability.availabilityState = state
            availability.loadDate = datetime.now()
            availability.save()
        return Response({"message": "Shedule deleted successfully."}, status=status.HTTP_201_CREATED)