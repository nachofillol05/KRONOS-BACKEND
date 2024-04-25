from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from .models import customuser
#from Serializers.userSR import UserSerializer
from django.core.mail import send_mail
from django.urls import reverse
from email.message import EmailMessage
import smtplib

# Create your views here.
class send_test_email(generics.GenericAPIView):
    def post(self,request):
        remitente = "proyecto.villada.solidario@gmail.com"
        destinatario = "weigandttimoteo@gmail.com"
        mensaje = "¡Hola, mundo!"
        email = EmailMessage()
        email["From"] = remitente
        email["To"] = destinatario
        email["Subject"] = "Ore no puede ser tan gay"
        email.set_content(mensaje)
        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, "bptf tqtv hjsb zfpl")
        smtp.sendmail(remitente, destinatario, email.as_string())
        smtp.quit()
        return Response('Correo electrónico enviado con éxito', status=200)
        

class LoginView(generics.GenericAPIView):
    #permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
              #  serializers = UserSerializer(user)
                login(request, user) 
                return Response({'message': 'Login exitoso'}, status=status.HTTP_200_OK) # Porque Response y no httpResponse
            else:
                return Response({'message': 'El usuario o contraseña son incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'message': 'An error occurred during login: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RegisterView(generics.GenericAPIView):
    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            #TENGO QUE CREAR UN USUARIO PERO EN LA BASE DE DATOS NO EL SISTEMA DE CISCO O MODIFICAR EL DE CISCO
            user = customuser.objects.create_user(username=username, email=email, password=password)
            print("el usuario es:" ,user)

            verification_url = request.build_absolute_uri(
                reverse('verify-email', args=[str(user.verification_token)])
            )
            send_mail(
                'Verifica tu correo electrónico',
                'Haz clic en el enlace para verificar tu correo electrónico: ' + verification_url,
                'from@example.com',
                [user.email],
            )
            return Response('Correo electrónico enviado con éxito', status=200)

            return Response('Usuario creado con éxito', status=200)


def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.email_verified = True
        user.save()
        return Response('Correo electrónico verificado con éxito')
    except User.DoesNotExist:
        return Response('Token de verificación no válido', status=400)