from ..models import(
    CustomUser,
    School,
    TeacherSubjectSchool,
    Year, 
    CourseSubjects,
    DocumentType,
    TeacherAvailability,
    AvailabilityState
)
from django.http import HttpResponse, JsonResponse, FileResponse
from django.conf import settings
from django.db.models import Q, Case, When
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from email.message import EmailMessage
from validate_email_address import validate_email
import smtplib
import pandas as pd
from pandas.errors import EmptyDataError
from ..utils import register_user
from ..serializers.school_serializer import ReadUserSchoolSerializer
from ..serializers.teacher_serializer import TeacherSerializer
from ..serializers.preceptor_serializer import PreceptorSerializer
from ..serializers.user_serializer import UserSerializer
from ..serializers.year_serializer import YearSerializer
from ..serializers.teacherSubSchool_serializer import TeacherSubjectSchoolSerializer
from ..serializers.teacherAvailability_serializer import TeacherAvailabilitySerializer, AvailabilityStateSerializer
from ..serializers.auth_serializer import RegisterTeacherSubjectSchoolSerializer
from ..utils import send_email



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

        queryset = TeacherSubjectSchool.objects.filter(school=request.school).exclude(teacher__document=11111111)
        
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

class DniComprobation(generics.GenericAPIView):
    '''
    COMPROBACION SI EL PROFESOR EXISTE ANTES DE CREAR UN NUEVO PROFESOR
    '''
    def post(self, request):
            document = request.data.get('document')
            documentType = request.data.get('documentType')
            print(document,documentType)
            user = CustomUser.objects.filter(documentType=documentType, document=document)

            if user.exists():
                user = user.first()
                serializer = TeacherSerializer(user)
                return Response({'results': 'DNI en uso', 'user': serializer.data}, status=400)
            else:
                return Response({'results': 'DNI no está en uso'}, status=200)

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
    

class ContactarPersonal(generics.GenericAPIView):
    def post(self, request):
        subject = request.data.get('asunto')
        message = request.data.get('contenido')
        recivers = request.data.get('teacher_mail')  # Usamos get en lugar de getlist

        if not recivers:
            return Response({'detail': 'teacher_mail is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not subject or not message:
            return Response({'detail': 'subject and message are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si solo es un string (un solo correo), lo convertimos en una lista
        if isinstance(recivers, str):
            recivers = [recivers]

        # Asegurarse de que recivers sea una lista
        if not isinstance(recivers, list):
            return Response({'detail': 'teacher_mail must be a string or a list of emails'}, status=status.HTTP_400_BAD_REQUEST)
        
        send_email(recivers, subject, message)
        return Response({'detail': 'Email enviado correctamente'}, status=status.HTTP_200_OK)



     

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
    permission_classes = [IsAuthenticated, SchoolHeader]
    serializer_class = TeacherAvailabilitySerializer

    def get_queryset(self):
        user: CustomUser = self.request.user
        school = self.request.school

        teacher_id = self.request.query_params.get('teacher_id')
        necessary_role = user.is_directive(school) or user.is_preceptor(school)
        if teacher_id and necessary_role: 
            queryset = TeacherAvailability.objects.filter(
                module__school=self.request.school,
                teacher_id=teacher_id
            )
        else:
            queryset = TeacherAvailability.objects.filter(
                module__school=self.request.school,
                teacher=self.request.user
            )
        queryset = queryset.annotate(
            weekday=Case(
               When(module__day='lunes', then=1), 
               When(module__day='martes', then=2),
               When(module__day='miércoles', then=3),
               When(module__day='jueves', then=4),
               When(module__day='viernes', then=5),
            )
        ).order_by('weekday','module__startTime','module__moduleNumber')
        return queryset
       

    def filter_queryset(self, queryset):
       day = self.request.query_params.get('day')
       if day:
           queryset = queryset.filter(module__day=day)
       return queryset

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            return super().get_serializer(*args, **kwargs)
        
        if isinstance(kwargs.get('data'), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data
        
        # Verifica si es una lista o un solo objeto
        if isinstance(data, list):
            print("toma la lista")
            for item in data:
                item['teacher'] = request.user.pk
        else:
            data['teacher'] = request.user.pk

        # Si es una lista, se procesa cada uno
        if isinstance(data, list):
            response_data = []
            for item in data:
                # Busca si ya existe una entrada para el mismo teacher y module
                teacher = request.user
                module_id = item.get('module_id')
                existing_record = TeacherAvailability.objects.filter(teacher=teacher, module_id=module_id).first()

                if existing_record:
                    print("ACTUALIZA")
                    serializer = self.get_serializer(existing_record, data=item, partial=True)
                else:
                    print("CREA UNO NUEVO")
                    serializer = self.get_serializer(data=item)
                
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                response_data.append(serializer.data)

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            print("no toma la lista")
            return Response(serializer.data, status=status.HTTP_201_CREATED)



    
class TeacherAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, SchoolHeader]
    serializer_class = TeacherAvailabilitySerializer

    def get_queryset(self):
        return TeacherAvailability.objects.filter(module__school=self.request.school)

    def get_object(self):
        obj: TeacherAvailability = super().get_object()
        user = self.request.user
        
        if obj.teacher != user:
            raise PermissionDenied("No tienes permiso para acceder a este recurso.")
        return obj

    def get_serializer(self, *args, **kwargs):
        kwargs['data']['teacher'] = self.request.user.pk
        return super().get_serializer(*args, **kwargs)


class AvailabilityStateView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AvailabilityState.objects.all()
    serializer_class = AvailabilityStateSerializer


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

        df = df.rename(columns={
            'user_id': 'ID de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'phone': 'Teléfono',
            'roles': 'Roles'
        })

        # Crear un archivo Excel en la memoria utilizando un buffer
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=PersonalEscuela.xlsx'
        # Escribir el DataFrame en un archivo Excel usando openpyxl (por defecto)
        df.to_excel(response, index=False, sheet_name='Personal')
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
            user_dict = dict(UserSerializer(user).data)
            if user.is_directive(school):
                roles.append('Directivo')
            if user.is_teacher(school):
                roles.append('Profesor')
                teacher_availability = TeacherAvailabilitySerializer(
                    user.get_teacher_availability(school),
                    many=True
                ).data
                user_dict['teacher_availability'] = teacher_availability
            if user.is_preceptor(school):
                roles.append('Preceptor')
    
            if roles:
                user_dict["roles"] = roles
                if user.document != '11111111':
                    user_roles.append(user_dict) 

        return user_roles
    
class SchoolRolesView(APIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]
    serializarizer_class = RegisterTeacherSubjectSchoolSerializer

    def post(self, request):
        rol = request.data.get('role')
        user = request.data.get('user_id')
        year = request.data.get('year_id')

        if not rol:
            return Response({'detail': 'rol is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if rol == 'Profesor':
            data = {
                'teacher': user,
                'school': request.school.pk
            }
            serializerschool = RegisterTeacherSubjectSchoolSerializer(data=data)
            if not serializerschool.is_valid():
                return Response(serializerschool.errors, status=status.HTTP_400_BAD_REQUEST)
            serializerschool.save()
            return Response(serializerschool.data, status=status.HTTP_201_CREATED)

        if rol == 'Preceptor':
            if not year:
                return Response({'detail': 'year is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                year_instance = Year.objects.get(pk=year)
            except Year.DoesNotExist:
                return Response({'detail': 'Year does not exist'}, status=status.HTTP_404_NOT_FOUND)
            if year_instance.school != request.school:
                return Response({'detail': 'Year not recognized at school'}, status=status.HTTP_400_BAD_REQUEST)

            year_instance.preceptors.add(user)
            year_instance.save()

            return Response(f'user id: {user} asignado como preceptor de {year_instance}', status=status.HTTP_200_OK)

        if rol == 'Directivo':
            school = request.school
            school.directives.add(user)
            return Response(f'user id: {user} asignado como directivo', status=status.HTTP_200_OK)
        
        return Response({'detail': 'Role not recognized'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        
        rol = request.data.get('role')
        user = request.data.get('user_id')
        year = request.data.get('year_id')

        if not rol:
            return Response({'detail': 'rol is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user:
            return Response({'detail': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if rol == 'Preceptor':
            if not year:
                return Response({'detail': 'year is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            year_instance = Year.objects.get(pk=year)
            if year_instance.school != request.school:
                return Response({'detail': 'Year not recognized at school'}, status=status.HTTP_400_BAD_REQUEST)

            year_instance.preceptors.remove(user)
            year_instance.save()

            return Response(f'user id: {user} removido como preceptor de {year_instance}', status=status.HTTP_200_OK)
        
        elif rol == 'Directivo':
            school = request.school
            school.directives.remove(user)
            return Response(f'user id: {user} removido como directivo', status=status.HTTP_200_OK)
        
        elif rol == 'Profesor':
            try:
                teacher_subject_school = TeacherSubjectSchool.objects.get(teacher=user, school=request.school)
            except:
                return Response({'detail': 'Este Usuario no pertece a la escuela'}, status=status.HTTP_400_BAD_REQUEST)
            teacher_subject_school.delete()
            return Response(f'user id: {user} removido como profesor', status=status.HTTP_200_OK)
        
        else:
            return Response({'detail': 'Role not recognized'}, status=status.HTTP_400_BAD_REQUEST)
