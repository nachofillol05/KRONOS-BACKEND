from django.contrib.auth import authenticate, login, password_validation
from django.http import HttpResponse, JsonResponse, FileResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Case, When, IntegerField
from django.core.cache import cache
from django.core.exceptions import ValidationError as ValidationErrorDjango
from django.shortcuts import get_object_or_404
from datetime import datetime

from django.db import connection

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from datetime import datetime
from email.message import EmailMessage
from validate_email_address import validate_email
import smtplib
import pandas as pd
from pandas.errors import EmptyDataError
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from .schedule_creation import schedule_creation
from .utils import register_user, send_email
from .serializers.school_serializer import ReadUserSchoolSerializer, ReadSchoolSerializer, CreateSchoolSerializer, DirectiveSerializer, ModuleSerializer
from .serializers.teacher_serializer import TeacherSerializer, CreateTeacherSerializer
from .serializers.preceptor_serializer import PreceptorSerializer
from .serializers.user_serializer import UserSerializer, UpdateUserSerializer, UserWithRoleSerializer
from .serializers.Subject_serializer import SubjectWithCoursesSerializer
from .serializers.course_serializer import CourseSerializer
from .serializers.cousesubject_serializer import CourseSubjectSerializer
from .serializers.year_serializer import YearSerializer
from .serializers.module_serializer import ModuleSerializer
from .serializers.event_serializer import EventSerializer, EventTypeSerializer, CreateEventSerializer
from .serializers.documenttype_serializer import DocumentTypeSerializer
from .serializers.teacherSubSchool_serializer import TeacherSubjectSchoolSerializer
from .serializers.teacherAvailability_serializer import TeacherAvailabilitySerializer
from .serializers.roles_serializer import RoleSerializer
from .serializers.schedule_serializer import ScheduleSerializer
from .serializers.nationality_serializer import NationalitySerializer

from .models import(
    CustomUser,
    School,
    TeacherSubjectSchool,
    Subject,
    Year, 
    Module,
    Course,
    Schedules,
    Action,
    EventType,
    Event,
    CourseSubjects,
    DocumentType,
    TeacherAvailability,
    Nationality,
    Role
)


class LoginView(generics.GenericAPIView):
    '''
    INICIAR SESION
    '''
    def post(self, request):
        document = request.data.get('document')
        password = request.data.get('password')
        try:
            user = authenticate(request, document=document, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({'Token': token.key,'message': 'Login exitoso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'El usuario o contraseña son incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': 'Ocurrio un error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterView(generics.GenericAPIView):
    '''
    REGISTRAR USUARIOS
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    def post(self, request):
            created, results = register_user(data=request.data, request=request)
            status_code = status.HTTP_201_CREATED if created else status.HTTP_400_BAD_REQUEST
            return Response(results, status=status_code)

class VerifiedView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        return Response({"user_is_verified": user.email_verified}, 200)


class ExcelToteacher(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    '''
    DESCARGAR EXCEL CON EL FORMATO ADECUADO
    '''
    def get(self, request):
        file_path = settings.BASE_DIR / 'Static' / 'Profesores.xls'
        if file_path.exists():
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='Profesores.xls')
        else:
            return JsonResponse({'error': 'Archivo no encontrado'}, status=404)
    '''
    REGISTRAR USUARIOS EN CANTIDAD DESDE UN EXCEL
    '''
    def post(self, request):
        archivo = request.FILES.get('archivo') 
        if not archivo:
            return JsonResponse({'error': 'No se proporcionó un archivo'}, status=400)
        
        try:
            df = pd.read_excel(archivo, sheet_name=0, header=0, skiprows=[1])
        except EmptyDataError:
            return JsonResponse({'error': 'El archivo está vacío o tiene un formato incorrecto'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error al procesar el archivo: {str(e)}'}, status=500)

        try:
            dni = DocumentType.objects.get(name='DNI').id
            pasaporte = DocumentType.objects.get(name='Pasaporte').id
            cuit = DocumentType.objects.get(name='CUIT').id
        except DocumentType.DoesNotExist:
            raise ValidationError("El tipo de documento no se encuentra.")
        results = []

        for index, row in df.iterrows():
            if pd.notnull(row['Documento']):
                document = row['Documento']
                first_name = row['NOMBRE']
                last_name = row['APELLIDO']
                email = row['MAIL']
                phone = row['Telefono']
                tipo_documento = row['Tipo de Documento']

                if tipo_documento == 'DNI':
                    documentType = dni
                elif tipo_documento == 'Pasaporte':
                    documentType = pasaporte
                elif tipo_documento == 'CUIT':
                    documentType = cuit 
                else:
                    results.append({'Documento': document, 'Response': 'Tipo de documento no válido'})
                    continue

                if validate_email(email):
                    data = {
                        'email' : email,
                        'password': "contraseña",
                        'first_name': first_name,
                        'last_name': last_name,
                        'documentType': documentType,
                        'document': document,
                        'phone': phone,
                    }
                    result = register_user(data=data, request=request)
                    results.append({'Documento': document, 'Response': result})
                else:
                    results.append({'Documento': document, 'Response': 'Email no valido'})
                    
        if results:
            return JsonResponse({'results': results})
        else:
            return JsonResponse({'error': 'No se procesaron datos válidos'}, status=400)




class OlvideMiContrasenia(generics.GenericAPIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({"error": "Se requiere email en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "email no reconocido no válido"}, status=404)
        
        subject = 'Restablecer contraseña'
        verification_url = request.build_absolute_uri(
            reverse('forgot-password', args=[str(user.verification_token)])
        )
        message = 'Haz clic en el enlace para cambiar tu contrasenia: ' + verification_url 

        try:
            send_email(message=message, subject=subject, receiver=user.email)
        except smtplib.SMTPException as e:
            return {"error": "Error al enviar correo"}

        return Response('Correo enviado con exito', status=200)


def reset_password(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)

        if not user.email_verified:
            return Response({"error": "Email no verificado"}, status=400)

        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"error": "Debe pasar una nueva contraseña"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()
        return Response({'result': 'Contraseña cambiada'}, status=200)    
            
    except CustomUser.DoesNotExist:
        return Response({"error": "Token de verificación no válido"}, status=404)
    

class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password:
            return Response({"error": "Se requiere el campo 'current_password' en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({"error": "Se requiere el campo 'new_password' en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if not user.check_password(current_password):
            return Response({'error': 'La contraseña actual es incorrecta.'})
        
        try:
            password_validation.validate_password(new_password, user)
        except ValidationErrorDjango:
            return Response({"error": "Contraseña invaida"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({"message": "Contraseña actualizada con éxito."}, status=status.HTTP_200_OK)


class ProfileView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader]
    serializer_class = UserSerializer
    """
    Vista para obtener el perfil de un usuario
    """
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        date = datetime.now().strftime('%Y-%m-%d')
        school = request.school
        
        with connection.cursor() as cursor:
            sql_query = """
                SELECT COUNT(*)
                FROM (
                    SELECT sh.id as id,
                        sh.date,
                        tss.teacher_id as teacher_id,
                        sc.id school,
                        RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                    FROM Kronosapp_schedules sh
                    INNER JOIN Kronosapp_teachersubjectschool tss
                        ON sh.tssId_id = tss.id
                    INNER JOIN Kronosapp_coursesubjects cs
                        ON tss.coursesubjects_id = cs.id
                    INNER JOIN Kronosapp_customuser t
                        ON tss.teacher_id = t.id
                    INNER JOIN Kronosapp_school sc
                        ON tss.school_id = sc.id
                    INNER JOIN Kronosapp_subject s
                        ON cs.subject_id = s.id
                    WHERE DATE(sh.`date`) <= %s
                    AND t.id = %s
                    AND sc.id = %s
                ) as t
                WHERE t.RN = 1;
            """
            cursor.execute(sql_query, [date, user.id, school.id])
            results = cursor.fetchall()
            if results:
                data['hoursToWorkBySchool'] = results[0][0]
        countSchool = TeacherSubjectSchool.objects.filter(teacher=user).values('school').distinct().count()
        print(countSchool)
        if countSchool > 1:
            with connection.cursor() as cursor:
                sql_query = """
                    SELECT COUNT(*)
                    FROM (
                        SELECT sh.id as id,
                            sh.date,
                            tss.teacher_id as teacher_id,
                            sc.id school,
                            RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                        FROM Kronosapp_schedules sh
                        INNER JOIN Kronosapp_teachersubjectschool tss
                            ON sh.tssId_id = tss.id
                        INNER JOIN Kronosapp_coursesubjects cs
                            ON tss.coursesubjects_id = cs.id
                        INNER JOIN Kronosapp_customuser t
                            ON tss.teacher_id = t.id
                        INNER JOIN Kronosapp_school sc
                            ON tss.school_id = sc.id
                        INNER JOIN Kronosapp_subject s
                            ON cs.subject_id = s.id
                        WHERE DATE(sh.`date`) <= %s
                        AND t.id = %s
                    ) as t
                    WHERE t.RN = 1;
                """
                cursor.execute(sql_query, [date, user.id])
                results = cursor.fetchall()
                if results:
                    data['hoursToWork'] = results[0][0]
        else:
             data['hoursToWork'] = data['hoursToWorkBySchool']

        return Response(data, status=status.HTTP_200_OK)
    """
    Vista para acualizar los datos de un usuario
    """
    def put(self, request):
        usuario = request.user
        serializer = UpdateUserSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class SchoolView(generics.RetrieveUpdateAPIView):
    '''
    VISTA PARA OBTENER LAS ESCUELAS DEL DIRECTIVO
    '''
    serializer_class = ReadSchoolSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get_object(self):
        return self.request.school


class UserSchoolsView(generics.ListAPIView):
    '''
    VISTA PARA OBTENER LAS ESCUELAS DEL DIRECTIVO
    '''
    queryset = School.objects.all()
    serializer_class = ReadUserSchoolSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user:
            schools = set()

            # Obtener escuelas donde el usuario es profesor
            tss = TeacherSubjectSchool.objects.filter(teacher=user).distinct()
            for ts in tss:
                schools.add(ts.school)

            # Obtener escuelas donde el usuario es directivo
            dir_schools = School.objects.filter(directives=user).distinct()
            for school in dir_schools:
                schools.add(school)

            # Serializar la lista de escuelas
            serializer = self.get_serializer(schools, many=True)
            return Response(serializer.data)

        return Response({"error": "Usuario no encontrado"}, status=404)


class TeacherListView(generics.ListAPIView):
    '''
    VISTA PARA OBTENER LOS PROFESORES DE UNA ESCUELA, CON FILTRO DE MATERIAS Y NOMBRE O APELLIDO
    '''
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request, *args, **kwargs):
        subject_id = request.GET.get('subject_id')
        search_name = request.GET.get('search_name')

        queryset = TeacherSubjectSchool.objects.filter(school=request.school)
        
        if subject_id:
            queryset = queryset.filter(coursesubjects__subject__id=subject_id).distinct()

        if search_name:
            queryset = queryset.filter(
                teacher__first_name__icontains=search_name) | queryset.filter(
                teacher__last_name__icontains=search_name)


        if not queryset.exists():
            return Response({'error': 'No se encontraron maestros'}, status=404)
        teachers = []
        for ts in queryset:
            teacher = ts.teacher
            if teacher not in teachers:
                teachers.append(teacher)

        serializer = self.get_serializer(teachers, many=True)

        return Response(serializer.data)


#


class DniComprobation(generics.GenericAPIView):
    '''
    COMPROBACION SI EL PROFESOR EXISTE ANTES DE CREAR UN NUEVO PROFESOR
    '''
    def post(self, request):
            document = request.data.get('document')
            user = CustomUser.objects.filter(document=document)

            if user.exists():
                user = user.first()
                serializer = TeacherSerializer(user)
                return Response({'results': 'DNI en uso', 'user': serializer.data}, status=400)
            else:
                return Response({'results': 'DNI no está en uso'}, status=200)



class SubjectListCreate(generics.ListCreateAPIView):
    '''
    LISTAR Y CREAR MATERIAS
    '''
    queryset = Subject.objects.all()
    serializer_class = SubjectWithCoursesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        teacher = request.query_params.get('teacher')
        name = request.query_params.get('name')
        school = self.request.school
        
        queryset = Subject.objects.filter(coursesubjects__course__year__school=school).distinct()
        
        if start_time and end_time:
            queryset = queryset.filter(
                teachersubjectschool__schedules__module__startTime__gte=start_time,
                teachersubjectschool__schedules__module__endTime__lte=end_time
            ).distinct()
        
        if teacher:
            queryset = queryset.filter(
                teachersubjectschool__teacher__id=teacher
            ).distinct()
        
        if name:
            queryset = queryset.filter(name__icontains=name)

        if 'export' in request.GET and request.GET['export'] == 'excel':
            return self.export_to_excel(queryset)

        serializer = SubjectWithCoursesSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        course = validated_data.get('course')
        if course.year.school != self.request.school:
            raise ValidationError({'course': ['You can only modify the school you belong to']})
        serializer.save()

    def export_to_excel(self, queryset):
        # Convertir el queryset a un DataFrame de pandas
        data = list(queryset.values('id', 'name', 'abbreviation', 'color', 'coursesubjects__course__name'))

        df = pd.DataFrame(data)

        # Crear un archivo Excel en la memoria utilizando un buffer
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Subjects.xlsx'
        
        # Escribir el DataFrame en un archivo Excel usando pandas
        df.to_excel(response, index=False, sheet_name='Subjects')
        
        return response
    
    # def post(self, request):
    #     serializer = SubjectSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(
    #         {'Saved': 'La materia ha sido creada', 'data': serializer.data},status=status.HTTP_201_CREATED)


class SubjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectWithCoursesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'La materia ha sido eliminada'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'La materia ha sido actualizada', 'data': response.data}, status=status.HTTP_200_OK)




class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    

    def get(self, request):
        school = self.request.school
        queryset = Course.objects.filter(year__school = school).order_by('year__number', 'name')
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        year_number = request.data.get('year')

        # Verificar si el año existe utilizando el campo 'number'
        try:
            year = Year.objects.get(number=year_number)
        except Year.DoesNotExist:
            return Response({'Error': 'El año especificado no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear un diccionario mutable a partir de request.data
        data = request.data.copy()
        data['year'] = year

        # Crear el curso si el año existe
        serializer = CourseSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            {'Saved': 'El curso ha sido creado', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'El curso ha sido eliminado'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'El curso ha sido actualizado', 'data': response.data}, status=status.HTTP_200_OK)

class CourseSubjectListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = CourseSubjects.objects.all()
    serializer_class = CourseSubjectSerializer
    
    def get_queryset(self):
        queryset = CourseSubjects.objects.filter(course__year__school = self.request.school)
        if not queryset.exists():
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return queryset
    
    def post (self, request, *args, **kwargs):
        serializer = CourseSubjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {'Saved': 'La materia se ha asignado a un curso', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )




class YearListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def get_queryset(self):
        queryset = Year.objects.filter(school=self.request.school).order_by('number')
        if not queryset.exists():
            return Response({'detail': 'not found'}, status=status.HTTP_404_NOT_FOUND)
        return queryset
    
    def perform_create(self, serializer):
        school = self.request.school
        serializer.save(school=school)

class YearRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'El año ha sido eliminado'}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'El año ha sido actualizado', 'data': response.data}, status=status.HTTP_200_OK)
    

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        school = validated_data.get('school')
        if school != self.request.school:
            raise ValidationError({'school': ['You can only modify the school you belong to']})
        serializer.save()

    def get_queryset(self):
        queryset = Module.objects.filter(school=self.request.school).order_by('moduleNumber')

        day = self.request.query_params.get('day')
        if day:
            queryset = queryset.filter(day=day)
        
        return queryset
        


class PreceptorsView(APIView):
    """
    Endpoints que realiza acciones sobre los preceptores del colegio indicado en la ruta
    """
    queryset = CustomUser.objects.all()
    serializer_class = PreceptorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

   
    def get(self, request, *args, **kwargs):
        school = self.request.school
        queryset  = CustomUser.objects.filter(year__school=school).distinct()

        search = request.query_params.get('search', None)
        year_id = request.query_params.get('year_id', None)
        if  year_id:
            if not Year.objects.filter(pk=year_id).exists():
                raise ValidationError('"year_id" no existe')
            queryset = queryset.filter(year__pk=year_id)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(document__startswith=search)
            )
            
        if not queryset.exists():
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PreceptorSerializer(queryset, many=True)
        return Response(serializer.data)    
    

    
    def post(self, request, *args, **kwargs):
        """
        Se le indica el año y el usuario que sera añadido como preceptor.
        Devuelve el año actualizado
        """
        return self.manage_user(request, is_add=True)
    
    def delete(self, request, *args, **kwargs):
        """
        Se le indica el año y el usuario que sera removido como preceptor.
        Devuelve el año actualizado
        """
        return self.manage_user(request, is_add=False)

    def manage_user(self, request, is_add):
        year_id = request.data.get('year_id')
        user_id = request.data.get('user_id')

        if not year_id or not user_id:
            return Response({'detail': 'year_id and user_id are requireds'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            year = Year.objects.get(pk=year_id)
            user = CustomUser.objects.get(pk=user_id)
        except (Year.DoesNotExist, CustomUser.DoesNotExist):
            return Response({'detail': 'Year or User do not exist'}, status=status.HTTP_404_NOT_FOUND)

        if year.school != request.school:
            return Response({'detail': 'Year not recognized at school'})

        if is_add:
            if user in year.preceptors.all():
                return Response({'detail': 'User is already a preceptor.'})
            year.preceptors.add(user)
            status_code = status.HTTP_201_CREATED
        else:
            if user not in year.preceptors.all():
                return Response({'error': 'The user is not associated with the year.'}, status=status.HTTP_400_BAD_REQUEST)
            year.preceptors.remove(user)
            status_code = status.HTTP_200_OK
        
        year.save()
        serializer = YearSerializer(year)
        return Response(serializer.data, status=status_code)
    

class verifyToken(APIView):
    def post(self, request):
        token = request.data.get('token')
        token = Token.objects.get(key=token)
        user = token.user

        return JsonResponse({'user': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'document': user.document, 'email_verified': user.email_verified, 'is_active': user.is_active, 'is_staff': user.is_staff, 'is_superuser': user.is_superuser, 'date_joined': user.date_joined, 'last_login': user.last_login, 'verification_token': user.verification_token, 'id': user.id})

class ContactarPersonal(generics.GenericAPIView):
    def post(self, request):
        remitente = "proyecto.villada.solidario@gmail.com"
        destinatario = request.data.get('email')
        titulo = request.data.get('asunto')
        contenido = request.data.get('contenido')
        
        mensaje = EmailMessage()
        mensaje["From"] = remitente
        mensaje["To"] = destinatario
        mensaje["Subject"] = titulo
        mensaje.set_content(contenido)
        
        try:
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp.login(remitente, "bptf tqtv hjsb zfpl")
            smtp.send_message(mensaje)
            smtp.quit()
            return Response({"message": "Correo enviado correctamente"}, status=status.HTTP_200_OK)
        except smtplib.SMTPException as e:
            return Response({"message": "Error al enviar el correo electrónico"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
          
class Newscheduleview(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        result = schedule_creation()
        modules = result[0]
        cache.set('schedule_result', modules, timeout=3600)  # Guardar por 1 hora
        return Response(result)
    

class NewScheduleCreation(generics.GenericAPIView):
    def post(self, request):
        results = cache.get('schedule_result')
        if results is None:
            return Response({'error': 'Schedule not found'}, status=404)
        else: 
            for module in results:
                # Acceso a los datos
                day = module['day']
                hour = module['hour']
                tss_id = module['tss_id']
                school_id = module['school_id']

                # Buscar el módulo correspondiente
                try:
                    module = Module.objects.get(day=day, moduleNumber=hour, school=school_id)
                except Module.DoesNotExist:
                    return Response({'error': f'Module for day {day} and hour {hour} not found'}, status=404)
                # Buscar el tss correspondiente
                try:
                    tss = TeacherSubjectSchool.objects.get(id=tss_id)
                except Module.DoesNotExist:
                    return Response({'error': f'Teacher not found'}, status=404)

                # Buscar la acción correspondiente
                try:
                    action = Action.objects.get(name="agregar materia")
                except Action.DoesNotExist:
                    return Response({'error': 'Action "agregar materia" not found'}, status=404)

                # Crear la instancia de Schedules
                newschedule = Schedules(date=datetime.now(), action=action, module=module, tssId=tss)
                newschedule.save()

            return Response({'message': 'Schedules created successfully'})  


class EventListCreate(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(school=self.request.school)

        current_time = datetime.now()
        queryset = queryset.annotate(
            event_status=Case(
                When(startDate__lte=current_time, endDate__gte=current_time, then=1),  # En Curso
                When(startDate__gt=current_time, then=2),  # Pendiente
                When(endDate__lt=current_time, then=3),  # Finalizado
                output_field=IntegerField(),
            )
        ).order_by('event_status', 'startDate')



        name = self.request.query_params.get('name', None)
        event_type = self.request.query_params.get('eventType', None)
        max_date = self.request.query_params.get('maxDate', None)
        roles = self.request.query_params.getlist('rolesIds', None)

        if name:
            queryset = queryset.filter(name__icontains=name)
        if event_type:
            queryset = queryset.filter(eventType_id=event_type)
        if max_date:
            try:
                max_date = max_date.replace('%2F', '/')
                max_date_parsed = datetime.strptime(max_date, '%d/%m/%Y')
                queryset = queryset.filter(startDate__lte=max_date_parsed)
            except ValueError:
                raise ValidationError("La fecha proporcionada no tiene el formato correcto. Use 'dd/mm/yyyy'.")
        if roles:
            try:
                for role in roles:
                    role_id = int(role)
                    if not Role.objects.filter(pk=role_id).exists():
                        raise ValidationError({'error': '"roles_ids": no valido.'})
            except ValueError:
                    raise ValidationError("Los roles proporcionados no existen.")
                
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': 'Not found event.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            data = self.request.data
            data['school'] = self.request.school.pk
            kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventSerializer
        return CreateEventSerializer
    
    def perform_create(self, serializer):
        serializer.save(school=self.request.school)
      

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventSerializer
        return CreateEventSerializer
        
    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'PUT':
            data = self.request.data
            data['school'] = self.request.school.pk
            kwargs['data'] = data
        return super().get_serializer(*args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(school=self.request.school)

class AffiliatedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def post(self, request, *args, **kwargs):
        """
        Se le indica el año y el usuario que sera añadido como preceptor.
        Devuelve el año actualizado
        """
        return self.manage_user(request, is_add=True)
    
    def delete(self, request, *args, **kwargs):
        """
        Se le indica el año y el usuario que sera removido como preceptor.
        Devuelve el año actualizado
        """
        return self.manage_user(request, is_add=False)

    def manage_user(self, request, is_add):
        event_id = request.data.get('event_id')
        user = request.user

        if not event_id:
            return Response({'detail': '"event_id" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            event: Event = Event.objects.get(pk=event_id)
        except (Year.DoesNotExist):
            return Response({'detail': 'Year or User do not exist'}, status=status.HTTP_404_NOT_FOUND)

        if event.school != request.school:
            return Response({'detail': 'Year not recognized at school'})

        if is_add:
            if user in event.affiliated_teachers.all():
                return Response({'detail': 'User is already a affiliated.'})
            event.affiliated_teachers.add(user)
            status_code = status.HTTP_201_CREATED
        else:
            if user not in event.affiliated_teachers.all():
                return Response({'error': 'The user is not associated with event.'}, status=status.HTTP_400_BAD_REQUEST)
            event.affiliated_teachers.remove(user)
            status_code = status.HTTP_200_OK
        
        event.save()
        return Response(status=status_code)


class EventTypeViewSet(generics.ListAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class RoleView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class DocumentTypeViewSet(generics.ListAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class TeacherSubjectSchoolListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = TeacherSubjectSchool.objects.all()
    serializer_class = TeacherSubjectSchoolSerializer

    def get_queryset(self):
        queryset = TeacherSubjectSchool.objects.filter(school=self.request.school)
        return queryset
    
    def post(self, serializer):
        course_subject_id = self.request.data.get('coursesubjects')
        teacher_id = self.request.data.get('teacher')
        school = self.request.school

        try:
            course_subject = CourseSubjects.objects.get(id=course_subject_id)
            teacher = CustomUser.objects.get(id=teacher_id)
        except (CourseSubjects.DoesNotExist, CustomUser.DoesNotExist, School.DoesNotExist) as e:
            raise ValidationError('La materia, Curso y Profesor deben existir')

        
        TeacherSubjectSchool.objects.create(
                coursesubjects=course_subject,
                teacher=teacher,
                school=school
            )
        return Response({"message": "Profesor asignado correctamente"}, status=status.HTTP_201_CREATED)

class TeacherSubjectSchoolDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = TeacherSubjectSchool.objects.all()
    serializer_class = TeacherSubjectSchoolSerializer


class TeacherAvailabilityListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = TeacherAvailability.objects.all()
    serializer_class = TeacherAvailabilitySerializer

    
class TeacherAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    queryset = TeacherAvailability.objects.all()
    serializer_class = TeacherAvailabilitySerializer


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
                           s.name,
                           s.color,
                           cs.subject_id,
                           RANK() over (PARTITION BY sh.module_id, cs.course_id order by sh.date DESC) as RN
                    FROM Kronosapp_schedules sh
                    INNER JOIN Kronosapp_teachersubjectschool tss
                           ON sh.tssId_id = tss.id
                    INNER JOIN Kronosapp_coursesubjects cs
                           ON tss.coursesubjects_id = cs.id
                    INNER JOIN Kronosapp_customuser t
                           ON tss.teacher_id = t.id
                    INNER JOIN Kronosapp_subject s
                           ON cs.subject_id = s.id
                    WHERE DATE(sh.`date`) <= %s
                ) as t
                WHERE t.RN = 1
                ORDER BY course_id, module_id
            """
            cursor.execute(sql_query, [date])
            results = cursor.fetchall()

            data = [
                {
                    "id": row[0],
                    "date": row[1],
                    "module_id": row[2],
                    "course_id": row[3],
                    "teacher_id": row[4],
                    "nombre": row[5],
                    "profile_picture": row[6],
                    "subject_name": row[7],
                    "subject_color": row[8],
                    "subject_id": row[9]
                }
                for row in results
            ]


            if teacher_ids is not None:
                data = [row for row in data if row["teacher_id"] in teacher_ids]

            if course_ids is not None:
                data = [row for row in data if row["course_id"] in course_ids]
            

        return Response(data)


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

        validate_course_subjects = []
        for course_subject in course_subjects:
            weeklyHours = Schedules.objects.filter(tssId__coursesubjects=course_subject).count()
            if weeklyHours < course_subject.weeklyHours:
                validate_course_subjects.append(course_subject)
                



        available_subjects = []
        for course_subject in validate_course_subjects:
            teacher_subject_school = TeacherSubjectSchool.objects.filter(coursesubjects=course_subject).first()
            if teacher_subject_school:
                teacher = teacher_subject_school.teacher

                if TeacherAvailability.objects.filter(teacher=teacher, module=module, availabilityState__isEnabled=True).exists():
                    available_subjects.append(course_subject.subject)

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
        
        created_schedules = []
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
            created_schedules.append(schedule)

        return Response({"message": "Schedule creado exitosamente"}, status=status.HTTP_201_CREATED)

    

class UserRolesViewSet(APIView):
    permission_classes = [IsAuthenticated, SchoolHeader]

    def get(self, request):
        user = request.user
        school = request.school

        roles = []
        if user.is_directive(school):
            roles.append('Directivo')
        if user.is_teacher(school):
            roles.append('Profesor')
        if user.is_preceptor(school):
            roles.append('Preceptor')

        return Response({
            'roles': roles
        })
    

class SchoolStaffAPIView(APIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request):
        school = request.school
        user_data = self.get_staff_roles(school)
        # serializer = UserWithRoleSerializer(user_data, many=True)
        return Response(user_data, status=status.HTTP_200_OK)
    
    def get_staff_roles(self, school):
        user_roles = []
        users = CustomUser.objects.all()
        for user in users:
            roles = []
            if user.is_directive(school):
                roles.append('Directivo')
            if user.is_teacher(school):
                roles.append('Profesor')
            if user.is_preceptor(school):
                roles.append('Preceptor')

            if roles:
                user_dict = dict(UserSerializer(user).data)
                user_dict["roles"] = roles
                user_roles.append(user_dict)

        return user_roles


class StaffToExel(APIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request):
        school = request.school
        users = CustomUser.objects.all()
        roles_data = []

        for user in users:
            roles = []
            if user.is_directive(school):
                roles.append('Directivo')
            if user.is_teacher(school):
                roles.append('Profesor')
            if user.is_preceptor(school):
                roles.append('Preceptor')
            
            if roles:
                roles_data.append({
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone': user.phone,
                    'roles': ", ".join(roles)
                })

        return self.export_to_excel(roles_data)

    def export_to_excel(self, roles_data):
        df = pd.DataFrame(roles_data)
        # Crear un archivo Excel en la memoria utilizando un buffer
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=SchoolStaff.xlsx'
        # Escribir el DataFrame en un archivo Excel usando openpyxl (por defecto)
        df.to_excel(response, index=False, sheet_name='Staff')
        return response

class DirectivesView(APIView):
    """
    Endpoints que realizan acciones sobre los directivos del colegio indicado en la ruta
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request, *args, **kwargs):
        school = self.request.school    
        directives = school.directives.all()
        # filtros
        search = request.query_params.get('search', None)
        if search:
            directives = directives.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(document__startswith=search)
            )
            
        if not directives.exists():
            return Response({"error": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(directives, many=True)
        return Response(serializer.data)    

    def post(self, request, *args, **kwargs):
        """
        Se indica el usuario que será añadido como directivo.
        Devuelve la escuela actualizada.
        """
        return self.manage_directive(request, is_add=True)
    
    def delete(self, request, *args, **kwargs):
        """
        Se indica el usuario que será removido como directivo.
        Devuelve la escuela actualizada.
        """
        return self.manage_directive(request, is_add=False)

    def manage_directive(self, request, is_add):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        school = self.request.school

        if is_add:
            if user in school.directives.all():
                return Response({'detail': 'User is already a directive.'})
            school.directives.add(user)
            status_code = status.HTTP_201_CREATED
        else:
            if user not in school.directives.all():
                return Response({'error': 'The user is not associated as a directive.'}, status=status.HTTP_400_BAD_REQUEST)
            school.directives.remove(user)
            status_code = status.HTTP_200_OK
        
        school.save()
        serializer = ReadUserSchoolSerializer(school)
        return Response(serializer.data, status=status_code)


class NationalityViewSet(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    