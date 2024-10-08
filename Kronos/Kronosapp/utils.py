from django.contrib.auth import get_user_model
from django.urls import reverse
from email.message import EmailMessage
import smtplib
from .serializers.auth_serializer import RegisterSerializer, RegisterTeacherSubjectSchoolSerializer
from PIL import Image
from io import BytesIO
import base64
from .models import CustomUser
from django.http import HttpResponse



user = get_user_model()

def send_email(receivers, subject, message, sender="proyecto.villada.solidario@gmail.com"):
    email = EmailMessage()
    email["From"] = sender
    if isinstance(receivers, list):
        email["To"] = ", ".join(receivers)
    else:
        email["To"] = receivers
    
    email["Subject"] = subject
    email.set_content(message)
    
    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(sender, "bptf tqtv hjsb zfpl")
    
    smtp.sendmail(sender, receivers if isinstance(receivers, list) else [receivers], email.as_string())
    
    smtp.quit()

def register_user(request, data):
    serializer = RegisterSerializer(data=data)
    if not serializer.is_valid():
        return False, serializer.errors
    user = serializer.save()




    verification_url = f"http://localhost:3000/mailverificado/{user.verification_token}"
    SUBJECT = "Verifica tu correo electrónico"
    MESSAGE = 'Haz clic en el enlace para verificar tu correo electrónico: ' + verification_url
    send_email(receivers=user.email, subject=SUBJECT, message=MESSAGE)
    return True, serializer.data


def verify_email(request,token):
    try:
        print(token)
        user = CustomUser.objects.get(verification_token=token)
        print(user)
        if user.email_verified:
            return HttpResponse('Correo electrónico ya verificado', status=400)
        else:
            user.email_verified = True
            user.save()
            return HttpResponse('Correo electrónico verificado con éxito', status=200)
    except CustomUser.DoesNotExist:
        return HttpResponse('Token de verificación no válido', status=404)


def convert_image_to_binary(image_file):
    image = Image.open(image_file)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()


def convert_binary_to_image(binary_data):
    image_stream = BytesIO(binary_data)
    image = Image.open(image_stream)
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{image_base64}"
