from ..models import(
    CustomUser,
    School,
    TeacherSubjectSchool,
    DocumentType,
    Nationality
)
from django.contrib.auth import authenticate, login, password_validation
from django.contrib.auth.password_validation import validate_password 
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as ValidationErrorDjango
from django.db import connection
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..permissions import SchoolHeader, IsDirectiveOrOnlyRead
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from datetime import datetime
import smtplib
from ..utils import register_user, send_email
from ..serializers.school_serializer import ReadSchoolSerializer
from ..serializers.user_serializer import UserSerializer, UpdateUserSerializer, ProfilePictureUpdateSerializer
from ..serializers.documenttype_serializer import DocumentTypeSerializer
from ..serializers.nationality_serializer import NationalitySerializer



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
    

class OlvideMiContrasenia(generics.GenericAPIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({"error": "Se requiere email en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "email no reconocido no válido"}, status=404)
        
        """subject = 'Restablecer contraseña'
        verification_url = request.build_absolute_uri(
            reverse('forgot-password', args=[str(user.verification_token)])
        )
        message = 'Haz clic en el enlace para cambiar tu contrasenia: ' + verification_url """

        verification_url = f"http://localhost:3000/recuperarContrasenia/{user.verification_token}"
        subject = "Verifica tu correo electrónico"
        message = 'Haz clic para recuperar la contraseña: ' + verification_url

        try:
            send_email(message=message, subject=subject, receivers=user.email)
        except smtplib.SMTPException as e:
            return {"error": "Error al enviar correo"}

        return Response({'messaje': 'Correo enviado con exito'}, status=200)


class ResetPasswordView(APIView):

    def post(self, request, token):
        try:
            user = CustomUser.objects.get(verification_token=token)
        except CustomUser.DoesNotExist:
            return Response({"error": "Token de verificación no válido"}, status=404)

        if not user.email_verified:
            return Response({"error": "Email no verificado"}, status=400)
        
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"error": "Debe pasar un field 'new_password'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password)
        except ValidationErrorDjango as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(new_password)
        user.save()

        return Response({'result': 'Contraseña cambiada'}, status=200)
    

class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password:
            return Response({"error": "Se requiere el campo 'current_password' en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response({"error": "Se requiere el campo 'new_password' en el cuerpo de la solicitud."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        if not user.check_password(current_password):
            return Response({'error': 'La contraseña actual es incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            password_validation.validate_password(new_password, user)
        except ValidationErrorDjango as error:
            return Response({"detail": "Contraseña invalida", "error": error}, status=status.HTTP_400_BAD_REQUEST)
        
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



class UpdateProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = ProfilePictureUpdateSerializer

    def get_object(self):
        return self.request.user


class UserSchoolsView(generics.ListAPIView):
    '''
    VISTA PARA OBTENER LAS ESCUELAS DEL DIRECTIVO
    '''
    queryset = School.objects.all()
    serializer_class = ReadSchoolSerializer
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

            schools_preceptor = School.objects.filter(
                years__preceptors__pk=user.pk
            ).distinct()
            for school in schools_preceptor:
                schools.add(school)

            # Obtener escuelas donde el usuario es directivo
            dir_schools = School.objects.filter(directives=user).distinct()
            for school in dir_schools:
                schools.add(school)

            # Serializar la lista de escuelas
            serializer = self.get_serializer(schools, many=True)
            return Response(serializer.data)

        return Response({"error": "Usuario no encontrado"}, status=404)


class verifyToken(APIView):
    def post(self, request):
        token = request.data.get('token')
        token = Token.objects.get(key=token)
        user = token.user

        return JsonResponse({'user': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'document': user.document, 'email_verified': user.email_verified, 'is_active': user.is_active, 'is_staff': user.is_staff, 'is_superuser': user.is_superuser, 'date_joined': user.date_joined, 'last_login': user.last_login, 'verification_token': user.verification_token, 'id': user.id})


class DocumentTypeViewSet(generics.ListAPIView):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class NationalityViewSet(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer
    

class RolesUserView(APIView):
    permission_classes = [IsAuthenticated, SchoolHeader, IsDirectiveOrOnlyRead]

    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        
        school = request.school
        
        roles = []
        if user.is_directive(school):
            roles.append('Directivo')
        if user.is_teacher(school):
            roles.append('Profesor')
        if user.is_preceptor(school):
            roles.append('Preceptor')
        print(roles)

        if not roles:
            return Response({'error': 'Usuario sin relaciones'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "user_pk": user.pk,
                "roles": roles
            }, 
            status=status.HTTP_200_OK
        )
