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
from ..utils import call_free_teacher,call_free_subject


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
                    action = Action.objects.get(name="agregar materia")
                except Action.DoesNotExist:
                    return Response({'error': 'Action "agregar materia" not found'}, status=404)

                newschedule = Schedules(date=datetime.now(), action=action, module=module, tssId=tss)
                newschedule.save()

            return Response({'message': 'Schedules created successfully'})  


class ViewSchedule(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializer_class = ScheduleSerializer

    def get(self, request):
        date = self.request.query_params.get('date', None)
        teachers = self.request.query_params.getlist('teachers', None)
        courses = self.request.query_params.getlist('courses', None)

        if teachers:
            try:
                teacher_ids = [int(teacher) for teacher in teachers]
                for teacher_id in teacher_ids:
                    if not CustomUser.objects.filter(pk=teacher_id).exists():
                        raise ValidationError({'error': '"teachers_ids": no valido.'})
            except ValueError:
                raise ValidationError("Los teachers proporcionados no existen.")
        else:
            teacher_ids = None

        if courses:
            try:
                course_ids = [int(course) for course in courses]
                for course_id in course_ids:
                    if not Course.objects.filter(pk=course_id).exists():
                        raise ValidationError({'error': '"courses_ids": no valido.'})
            except ValueError:
                raise ValidationError("Los courses proporcionados no existen.")
        else:
            course_ids = None

        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        with connection.cursor() as cursor:
            sql_query = """
                SELECT *
                FROM (
                    SELECT sh.id as id,
                           sh.date,
                           sh.module_id,
                           cs.course_id as course_id,
                           tss.teacher_id as teacher_id,
                           CONCAT(t.first_name, ' ', t.last_name) AS nombre,
                           t.profile_picture,
                           s.abbreviation,
                           s.color,
                           cs.subject_id,
                           c.name as course_name,
                           m.day as day,
                           m.moduleNumber,
                           s.name as subject_name,
                           RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                    FROM Kronosapp_schedules sh
                    INNER JOIN Kronosapp_module m 
                            ON sh.module_id = m.id
                    INNER JOIN Kronosapp_teachersubjectschool tss
                           ON sh.tssId_id = tss.id
                    INNER JOIN Kronosapp_coursesubjects cs
                           ON tss.coursesubjects_id = cs.id
                    INNER JOIN Kronosapp_customuser t
                           ON tss.teacher_id = t.id
                    INNER JOIN Kronosapp_subject s
                           ON cs.subject_id = s.id
                    INNER JOIN Kronosapp_course c 
                            ON cs.course_id = c.id
                    WHERE DATE(sh.`date`) <= %s
                ) as t
                WHERE t.RN = 1
                ORDER BY course_id, module_id
            """
            cursor.execute(sql_query, [date])
            results = cursor.fetchall()

            from ..utils import convert_binary_to_image
            data = []
            for row in results:
                if not row[13] == "freeSubject":
                    data.append({
                        "id": row[0],
                        "date": row[1],
                        "module_id": row[2],
                        "course_id": row[3],
                        "teacher_id": row[4],
                        "nombre": row[5],
                        "profile_picture": convert_binary_to_image(row[6]) if row[6] else None,
                        "subject_abreviation": row[7],
                        "subject_color": row[8],
                        "subject_id": row[9],
                        "course_name": row[10],
                        "day": row[11],
                        "moduleNumber": row[12],
                        "subject_name": row[13]
                    })

            if teacher_ids is not None:
                data = [row for row in data if row["teacher_id"] in teacher_ids]

            if course_ids is not None:
                data = [row for row in data if row["course_id"] in course_ids]
        return Response(data)

class ViewTeacherSchedule(generics.ListAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader]
    serializer_class = ScheduleSerializer
    def get(self, request):
        teacher_id = self.request.user.pk

        freeteacher = call_free_teacher()

        with connection.cursor() as cursor:
                sql_query = """
                    SELECT *
                    FROM (
                        SELECT sh.id as id,
                            sh.date,
                            sh.module_id,
                            cs.course_id as course_id,
                            tss.teacher_id as teacher_id,
                            s.abbreviation,
                            s.color,
                            cs.subject_id,
                            c.name as course_name,
                            m.day as day,
                            m.moduleNumber,
                            s.name as subject_name,
                            sc.logo,
                            sc.name,
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
                        WHERE DATE(sh.`date`) <= %s
                        AND t.id = %s OR t.id = %s
                    ) as t
                    WHERE t.RN = 1
                    AND t.teacher_id = %s
                    ORDER BY course_id, module_id	
                """
                cursor.execute(sql_query, [datetime.now(), teacher_id, freeteacher, teacher_id])
                results = cursor.fetchall()

                from ..utils import convert_binary_to_image
                data = []
                for row in results:
                    if not row[11] == "freeSubject":
                        data.append({
                            "id": row[0],
                            "date": row[1],
                            "module_id": row[2],
                            "course_id": row[3],
                            "teacher_id": row[4],
                            "subject_abreviation": row[5],
                            "subject_color": row[6],
                            "subject_id": row[7],
                            "course_name": row[8],
                            "day": row[9],
                            "moduleNumber": row[10],
                            "subject_name": row[11],
                            "logo": convert_binary_to_image(row[12]) if row[12] else None,
                            "school_name": row[13]
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
                            WHERE DATE(sh.`date`) <=  %s
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
                course_subject = CourseSubjects.objects.get(course=course_id, subject=subject_id)
                
                teacher_subject_school = TeacherSubjectSchool.objects.get(coursesubjects=course_subject, school=request.school)
                module = Module.objects.get(id=module_id)
            except CourseSubjects.DoesNotExist:
                return Response({"error": "CourseSubject no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            except TeacherSubjectSchool.DoesNotExist:
                return Response({"error": "TeacherSubjectSchool no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
            except Module.DoesNotExist:
                return Response({"error": "Módulo no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

            schedule = Schedules.objects.create(
                date=datetime.now(),
                action_id=None,
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

            state = AvailabilityState.objects.get(name="Asignado")
            availability = TeacherAvailability.objects.get(module=module, teacher=teacher_subject_school.teacher)
            availability.availabilityState = state
            availability.loadDate = datetime.now()  
            availability.save() 

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
                old_teacher =  [row[5] for row in cursor.fetchall()]
                teacher = int(old_teacher[0])

        
        print(old_teacher)
        
        if not module_id or not course_id:
            return Response({"error": "Se necesita pasar el ID del curso y el ID del módulo."}, status=status.HTTP_400_BAD_REQUEST)
        
        freesubject=call_free_subject(request.school)
        freeTeacher=call_free_teacher()
        try:
            module = Module.objects.get(pk=module_id)
        except Module.DoesNotExist:
            print("NO EXISTE EL MODULO")
            return Response({"error": "El modulo proporcionado no existe."}, status=status.HTTP_400_BAD_REQUEST)
        try: 
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            print("NO EXISTE EL CURSO")
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
            print("ELIMINA EL SHEDULE")
            schedule = Schedules.objects.create(
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
                print("NO EXISTE LA DISPONIBILIDAD DEL PROFESOR")
                return Response({"error": "No se encontro la disponibilidad del profesor."}, status=status.HTTP_404_NOT_FOUND)
            availability.availabilityState = state
            availability.loadDate = datetime.now()
            availability.save()
        return Response({"message": "Shedule deleted successfully."}, status=status.HTTP_201_CREATED)