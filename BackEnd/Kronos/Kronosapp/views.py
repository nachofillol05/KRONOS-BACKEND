from django.contrib.auth import authenticate
from rest_framework import generics
from django.http import HttpResponse
from .models import User
from django.core.mail import send_mail
from django.urls import reverse

# Create your views here.

class LoginView(generics.GenericAPIView):
    #permission_classes = [AllowAny]
    def post(self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return HttpResponse('Login exitoso', status=200)
            else:
                return HttpResponse('El usuario o la contraseña no existen', status=400)



class RegisterView(generics.GenericAPIView):
    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            #TENGO QUE CREAR UN USUARIO PERO EN LA BASE DE DATOS NO EL SISTEMA DE CISCO O MODIFICAR EL DE CISCO
            user = user.objects.create_user(username=username, email=email, password=password)
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

        return HttpResponse('Correo electrónico enviado con éxito', status=200)


def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.email_verified = True
        user.save()
        return HttpResponse('Correo electrónico verificado con éxito')
    except User.DoesNotExist:
        return HttpResponse('Token de verificación no válido', status=400)