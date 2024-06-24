from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.http import JsonResponse, FileResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db.models import Q
#from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from email.message import EmailMessage
from validate_email_address import validate_email
import smtplib
import pandas as pd
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from django.urls import reverse
from .models import CustomUser, School, TeacherSubjectSchool, Subject, Year, Module, Course

from .serializers.school_serializer import ReadSchoolSerializer, CreateSchoolSerializer, DirectiveSerializer, ModuleSerializer
from .serializers.teacher_serializer import TeacherSerializer, CreateTeacherSerializer
from .serializers.preceptor_serializer import PreceptorSerializer, YearSerializer
from .serializers.user_serializer import UserSerializer
from .serializers.Subject_serializer import SubjectSerializer



@extend_schema(
    tags=['Users'],
    description='Permite a un usuario existente iniciar sesión en el sistema.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'string',
                    'example': 'superusername'
                },
                'password': {
                    'type': 'string',
                    'format': 'password',
                    'example': 'pepe1234'
                }
            },
            'required': ['username', 'password']
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'token': {
                    'type': 'string',
                    'example': 'a18a0428a4d6cb797ba5923eb7315af9b8f182ad'
                },
                'message': {
                    'type': 'string',
                    'example': 'Login exitoso'
                    }
                }
            },
        401: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'El usuario o contraseña son incorrectos'
                },
            }
        },
        500: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'An error occurred during login'
                }
            }
        }
    }
)
class LoginView(generics.GenericAPIView):
    '''
    INICIAR SESION
    '''
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({'Token': token.key,'message': 'Login exitoso'}, status=status.HTTP_200_OK) # Porque Response y no httpResponse
            else:
                return Response({'message': 'El usuario o contraseña son incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': 'An error occurred during login: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(
    tags=['Users'],
    description="Registra un nuevo usuario. puede ser un profesor, un preceptor o un directivo.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'first_name': {
                    'type': 'string',
                    'example': 'Monica'
                },
                'last_name': {
                    'type': 'string',
                    'example': 'Flores'
                },
                'document': {
                    'type': 'string',
                    'example': '123456789'
                },
                'email': {
                    'type': 'string',
                    'example': 'micorreo@correo.com'
                },
                'password': {
                    'type': 'string',
                    'format': 'password',
                    'example': 'pepe1234'
                }
            },
            'required': ['first_name', 'last_name', 'document', 'email', 'password']
        }
    },
    responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {
                        'type': 'string',
                        'example': '354b333cfb962cfc4df0e8105e21275ad55e5450'
                    },
                    'mensaje': {
                        'type': 'string',
                        'example': 'Correo electrónico enviado con éxito'
                    }
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': 'Nombre de usuario ya en uso'
                    },
                    'err': {
                        'type': 'string',
                        'example': 'Mail ya en uso'
                    }
                }
            }
    }
)
class RegisterView(generics.GenericAPIView):
    '''
    REGISTRAR USUARIOS
    '''
    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = f"{first_name}_{last_name}"
        document = request.data.get('document')
        email = request.data.get('email')
        password = request.data.get('password')
        mensaje = send_email(request, username, email, password, document, first_name, last_name)
        return Response({'detail':mensaje}, status=status.HTTP_201_CREATED)






@extend_schema(
    tags=['Teachers'],
    description="Registra a los usuarios desde un archivo excel. El archivo debe tener un formato especifico.",
    request={
        'application/json': {
            'type': 'object',
            'propieties': {
                'file': {
                    'type': 'file',
                    'example': 'Profesores.xls'  
                }
            },               
        }
    }
)
class ExcelToteacher(generics.GenericAPIView):

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
        archivo = 'Static/Profesores.xls'
        df = pd.read_excel(archivo, sheet_name=0, header=0)
        results = []
        '''
        IMPLEMENTAR
        archivo = request.FILES.get('archvio') 
        if not archivo:
            return JsonResponse({'error': 'No se proporcionó un archivo'}, status=400)
        '''

        for index, row in df.iterrows():
            if pd.notnull(row['DNI']):
                print(row)
                document = row['DNI']
                username = row['NOMBRE'] + '_' + row['APELLIDO']
                first_name = row['NOMBRE']
                last_name = row['APELLIDO']
                email = row['MAIL']
                password = str(row['DNI'])

                if validate_email(email):
                    result = send_email(request, username, email, password, document, first_name, last_name)
                    results.append({'DNI': document, 'Response': result})
                else:
                    results.append({'DNI': document, 'Response': 'Email no valido'})

        if results:
            return JsonResponse({'results': results})
        else:
            return JsonResponse({'error': 'No se procesaron datos válidos'}, status=400)






def send_email(request, username, email, password, document, first_name, last_name):
    '''
    FUNCION CREAR USUARIOS Y MANDAR MAILS. LA LLAMAN DESDE: RegisterView y ExcelToteacher
    '''
    if CustomUser.objects.filter(username=username).exists():
        return 'Nombre de usuario ya en uso'
    else:
        if CustomUser.objects.filter(email=email).exists():
            return 'mail ya en uso'
        else:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, document=document)
            token = Token.objects.create(user=user)
            verification_url = request.build_absolute_uri(
            reverse('verify-email', args=[str(user.verification_token)])
            )
            remitente = "proyecto.villada.solidario@gmail.com"
            destinatario = user.email
            mensaje = 'Haz clic en el enlace para verificar tu correo electrónico: ' + verification_url
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = 'Verifica tu correo electrónico'
            email.set_content(mensaje)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remitente, "bptf tqtv hjsb zfpl")
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()
            return {"token":token.key,"mensaje":'Correo electrónico enviado con éxito'}


@extend_schema(
    tags=['Users'], 
    description="Permite a un usuario verificar su dirección de correo electrónico haciendo clic en un enlace enviado por email después del registro.",
    responses={
        200: {
            'type': 'object', 'properties': {
                'mensaje': {
                    'type': 'string',
                    'example': 'Correo electrónico verificado con éxito'
                }
            }
        },
        400: {
            'type': 'object', 'properties': {
                'mensaje': {
                    'type': 'string',
                    'example': 'Correo electrónico ya verificado'
                }
            }
        },
        401: {
            'type': 'object', 'properties': {
                'mensaje': {
                    'type': 'string',
                    'example': 'Token de verificación no válido'
                },
            }
        }
    }
)
@api_view(['GET'])
def verify_email(request,token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if user.email_verified:
            return HttpResponse('Correo electrónico ya verificado', status=400)
        else:
            user.email_verified = True
            user.save()
            return HttpResponse('Correo electrónico verificado con éxito', status=200)
    except CustomUser.DoesNotExist:
        return HttpResponse('Token de verificación no válido', status=404)


@extend_schema(
    tags=['Users'],
    description='Permite a un usuario solicitar un enlace para restablecer su contraseña. El token es el enviado en el REQUEST BODY con la key de "token". Por ejemplo: {"token": mitoken} para identificar el usuario.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'username': {
                    'type': 'string',
                    'example': 'superusername'
                },
                'password': {
                    'type': 'string',
                    'format': 'password',
                    'example': 'aguantebelgrano'
                }
            },
            'required': ['username', 'password']
        },
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'token': {
                    'type': 'string',
                    'example': 'a18a0428a4d6cb797ba5923eb7315af9b8f182ad'
                },
                'message': {
                    'type': 'string',
                    'example': 'Login exitoso'
                    }
                }
            },
        401: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'El usuario o contraseña son incorrectos'
                },
            }
        }
    }
)
class OlvideMiContrasenia(generics.GenericAPIView):
    def get(self, request):
        try:
            token = request.data.get('token')
            user = request.user
            token = Token.objects.get(key=token)
            user = token.user
            remitente = user.email
            verification_url = request.build_absolute_uri(
                reverse('forgot-password', args=[str(user.verification_token)])
            )
            remitente = "proyecto.villada.solidario@gmail.com"
            destinatario = user.email
            
            mensaje = 'Haz clic en el enlace para cambiar tu contrasenia: ' + verification_url
            email = EmailMessage()
            email["From"] = remitente
            email["To"] = destinatario
            email["Subject"] = 'Cambie su contraseña'
            email.set_content(mensaje)
            smtp = smtplib.SMTP_SSL("smtp.gmail.com")
            smtp.login(remitente, "bptf tqtv hjsb zfpl")
            smtp.sendmail(remitente, destinatario, email.as_string())
            smtp.quit()
            return Response('Correo enviado con exito', status=200)
        except:
            return Response('Error al enviar el correo', status=400)

@extend_schema(
    tags=['Users'],
    description='permite a un usuario restablecer su contraseña utilizando el token enviado por email.',
    responses={
        200: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'Contraseña cambiada'
                }
            }
        },
        400: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'El correo no esta verificado'
                }
            }
        },
        404: {
            'type': 'object',
            'properties': {
                'message': {
                    'type': 'string',
                    'example': 'Token de verificacion no valido'
                }
            }
        }
    }
)
@api_view(['POST'])
def change_password(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if user.email_verified:
            user.password = make_password('contrasenia temporal')#request.data.get('password') cuano se haga el front
            user.save()
            return Response('Contraseña cambiada', status=200)
        else:
            return Response('El correo no esta verificado', status=400)
            
    except CustomUser.DoesNotExist:
        return Response('Token de verificación no válido', status=404)


@extend_schema(tags=['Users'])
class ProfileView(generics.GenericAPIView):
    """
    Vista para obtener el perfil de un usuario autenticado
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(
        summary="Obtener información del perfil",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="No autenticado")
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Actualizar información del perfil",
        request=UserSerializer,
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        }
    )
    def put(self, request):
        usuario = request.user
        serializer = UserSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@extend_schema(tags=['Schools'])

class SchoolsView(generics.ListAPIView):
    '''
    VISTA PARA LAS ESCUELAS DE UN USUARIO
    '''
    queryset = School.objects.all()
    serializer_class = ReadSchoolSerializer
    def get_queryset(self):
        user = self.request.user
        schools = TeacherSubjectSchool.objects.filter(teacher=user).distinct()
        return schools
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
   

    
    


@extend_schema(tags=['Teachers'])
class TeacherListView(generics.ListAPIView):
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request, *args, **kwargs):

        subject_id = request.GET.get('subject_id')
        search_name = request.GET.get('search_name')

        queryset = TeacherSubjectSchool.objects.all()

        
        if subject_id:
            queryset = queryset.filter(subject_id=subject_id)

        if search_name:
            queryset = queryset.filter(
                teacher__first_name__icontains=search_name) | queryset.filter(
                teacher__last_name__icontains=search_name)


        if not queryset.exists():
            return Response({'error': 'No se encontraron maestros'}, status=404)
        teachers = []
        for ts in queryset:
            teacher = ts.teacher
            teachers.append(teacher)

        serializer = self.get_serializer(teachers, many=True)

        return Response(serializer.data)


@extend_schema(tags=['Teachers'])
class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        serializer = self.get_serializer(instance)
        return Response({'object_deleted': serializer.data})

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return ReadSchoolSerializer
        return CreateSchoolSerializer
        if self.request.method == 'PATCH':
            return CreateTeacherSerializer
        return super().get_serializer_class()


@extend_schema(tags=['Teachers'])
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



@extend_schema(tags=['Subjects'])

class SubjectListCreate(generics.ListCreateAPIView):
    '''
    LISTAR Y CREAR MATERIAS
    '''
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request):

        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        teacher = request.query_params.get('teacher')
        name = request.query_params.get('name')
        school = self.request.school
        
        queryset = Subject.objects.filter(course__year__school=school)
        # Filter by start_time and end_time
        if start_time and end_time:
            queryset = queryset.filter(
                teachersubjectschool__schedules__module__startTime__gte=start_time,
                teachersubjectschool__schedules__module__endTime__lte=end_time
            ).distinct()
        # Filter by teacher
        if teacher:
            queryset = queryset.filter(
                teachersubjectschool__teacher__id=teacher
            ).distinct()
        # Filter by subject name
        if name:
            queryset = queryset.filter(name__icontains=name)


        serializer = SubjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        course = validated_data.get('course')
        if course.year.school != self.request.school:
            raise ValidationError({'course': ['You can only modify the school you belong to']})
        serializer.save()
    
    # def post(self, request):
    #     serializer = SubjectSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(
    #         {'Saved': 'La materia ha sido creada', 'data': serializer.data},status=status.HTTP_201_CREATED)


@extend_schema(tags=['Subjects'])
class SubjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'Deleted': 'La materia ha sido eliminada'}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return Response({'Updated': 'La materia ha sido actualizada', 'data': response.data}, status=status.HTTP_200_OK)


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='day', description='Day of the week', required=False, type=str),
        ]
    )
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
        

@extend_schema(tags=['Preceptors'])
class PreceptorsView(APIView):
    """
    Endpoints que realiza acciones sobre los preceptores del colegio indicado en la ruta
    """
    queryset = CustomUser.objects.all()
    serializer_class = PreceptorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    @extend_schema(
        summary='Obtener preceptores de una escuela',
        responses={200: PreceptorSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        pk_school = self.kwargs.get('pk_school')
        preceptors = CustomUser.objects.filter(years__school=request.school).distinct()
        serializer = PreceptorSerializer(preceptors, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary='Agregar preceptor',
        request={
            'application/json': {

                'type': 'object',
                'properties': {
                    'year_id': {'type': 'integer'},
                    'user_id': {'type': 'integer'}
                },
                'required': ['year_id', 'user_id']
            }
        },
        responses={
            201: YearSerializer(),
            400: OpenApiResponse(description="year_id and user_id are requireds"),
            404: OpenApiResponse(description="Year or User do not exist")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Se le indica el año y el usuario que sera añadido como preceptor.
        Devuelve el año actualizado
        """
        return self.manage_user(request, is_add=True)
    
    @extend_schema(
        summary='Remover preceptor',
        request={
            'application/json': {

                'type': 'object',
                'properties': {
                    'year_id': {'type': 'integer'},
                    'user_id': {'type': 'integer'}
                },
                'required': ['year_id', 'user_id']
            }
        },
        responses={
            201: YearSerializer(),
            400: OpenApiResponse(description="year_id and user_id are requireds"),
            402: OpenApiResponse(description="The user is not associated with the year."),
            404: OpenApiResponse(description="Year or User do not exist")
        }
    )
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
        print(user)
        return JsonResponse({'user': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'document': user.document, 'email_verified': user.email_verified, 'is_active': user.is_active, 'is_staff': user.is_staff, 'is_superuser': user.is_superuser, 'date_joined': user.date_joined, 'last_login': user.last_login, 'verification_token': user.verification_token, 'id': user.id})
