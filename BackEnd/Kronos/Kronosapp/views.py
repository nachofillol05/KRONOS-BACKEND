from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .models import customuser, Schools
from .Serializers import SchoolSerializer
#from Serializers.userSR import UserSerializer
from django.urls import reverse
from email.message import EmailMessage
import smtplib
        
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
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            if customuser.objects.filter(username=username).exists():
                return Response('Nombre de usuario ya en uso', status=400)
            
            else:
                user = customuser.objects.create_user(username=username, email=email, password=password)
                verification_url = request.build_absolute_uri(
                reverse('verify-email', args=[str(user.verification_token)])
                )
                remitente = "proyecto.villada.solidario@gmail.com"
                destinatario = "nachofillol05@gmail.com"
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
                return Response('Correo electrónico enviado con éxito', status=200)
            
        except Exception as e:
            return Response({'message': 'Ocurrió un error durante el registro: ' + str(e)}, status=500)
        

            


def verify_email(request,token):
    try:
        user = customuser.objects.get(verification_token=token)
        if user.email_verified:
            return HttpResponse('Correo electrónico ya verificado', status=400)
        else:
            user.email_verified = True
            user.save()
            return HttpResponse('Correo electrónico verificado con éxito', status=200)
    except customuser.DoesNotExist:
        return HttpResponse('Token de verificación no válido', status=400)
    
# Definición de la vista para listar y crear School
class SchoolListCreateView(generics.ListCreateAPIView):

    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer

# Definición de la vista para recuperar, actualizar y eliminar School
class SchoolRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schools.objects.all()
    serializer_class = SchoolSerializer


