from django.contrib.auth import get_user_model
from django.urls import reverse
from email.message import EmailMessage
import smtplib
from .serializers.auth_serializer import RegisterSerializer, RegisterTeacherSubjectSchoolSerializer
from PIL import Image
from io import BytesIO
import base64
from .models import CustomUser, DocumentType, Nationality, ContactInformation, Subject
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response



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
    contact_info_empty = {
        "postalCode": "",
        "street": "",
        "streetNumber": "",
        "city": "",
        "province": ""
    }
    contact_info = ContactInformation.objects.create(**contact_info_empty)
    data['contactInfo'] = contact_info.pk
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

def call_free_teacher():
    try:
        freeTeacher = CustomUser.objects.get(document=11111111)
    except:
        try:
            document_type = DocumentType.objects.get(name="DNI")
        except DocumentType.DoesNotExist:
            return Response({"error": "El tipo de documento DNI no fue encontrado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            nationality = Nationality.objects.get(name="Argentina")
        except Nationality.DoesNotExist:
            return Response({"error": "El pais Argentina no fue encontrado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try: 
            contact_info = ContactInformation.objects.get(street="ProfesorLibre") 
        except ContactInformation.DoesNotExist:
            contact_info = ContactInformation.objects.create(
                postalCode = 111,
                street = "ProfesorLibre",
                streetNumber = 111,
                city = "Córdoba",
                province = "Córdoba"
            )
        freeTeacher = CustomUser.objects.create(
            document = 11111111,
            first_name = "Profesor",
            last_name = "Libre",
            gender = "Otro"   ,        
            email = "profesorlibre@gmail.com",
            hoursToWork = 999,
            phone = 3511111111,
            documentType = document_type,
            nationality = nationality,
            contactInfo =  contact_info,
            email_verified = True
        )
    return freeTeacher

def call_free_subject(school):
    try:
        freeSubject = Subject.objects.get(name = "freeSubject", school = school)
    except Subject.DoesNotExist:
        freeSubject = Subject.objects.create(
            name = "freeSubject",
            description = "A non-existent subject that is used when deleting a schedule",
            abbreviation = "Free",
            school = school
        )
    return freeSubject