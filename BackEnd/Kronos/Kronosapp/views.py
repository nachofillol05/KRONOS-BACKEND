from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from django.urls import reverse
from .models import CustomUser, School
from .serializers.school_serializer import ReadSchoolSerializer, CreateSchoolSerializer, DirectiveSerializer
from email.message import EmailMessage
import smtplib
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


class LoginView(generics.GenericAPIView):
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


class RegisterView(generics.GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if CustomUser.objects.filter(username=username).exists():
            return Response('Nombre de usuario ya en uso', status=400)
        
        else:
            if CustomUser.objects.filter(email=email).exists():
                return Response('mail ya en uso', status=400)
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
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
                return Response({"token":token.key,"mensaje":'Correo electrónico enviado con éxito'}, status=200)


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
        return HttpResponse('Token de verificación no válido', status=400)


class OlvideMiContrasenia(generics.GenericAPIView):
    def get(self, request):
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
    
def change_password(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        if user.email_verified:
            user.password = make_password('contrasenia temporal')#request.data.get('password') cuano se haga el front
            user.save()
            return HttpResponse('Contraseña cambiada', status=200)
        else:
            return HttpResponse('El correo no esta verificado', status=400)
            
    except CustomUser.DoesNotExist:
        return HttpResponse('Token de verificación no válido', status=400)


class SchoolListView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = ReadSchoolSerializer

class SchoolCreateView(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = CreateSchoolSerializer

    def get(self, request):
        queryset = CustomUser.objects.all()
        print(queryset)
        serializer = DirectiveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
class SchoolListView(generics.ListCreateAPIView):
    queryset = School.objects.all()
    
    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return ReadSchoolSerializer
        return CreateSchoolSerializer
"""