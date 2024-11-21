
from Kronosapp.models import (ContactInformation,CustomUser,DocumentType,Nationality)
from Kronosapp.management.commands.seed_images import *

def test_seed():
    # Fetch required related objects
    dni = DocumentType.objects.get(name="DNI")
    argentina = Nationality.objects.get(name="Argentina")
    nationalities = Nationality.objects.distinct()

    contact_info_preceptor_1ro = ContactInformation.objects.create(
                postalCode='5000',
                street='Avenida Colón',
                streetNumber='2345',
                city='Córdoba',
                province='Córdoba'
            )

    preceptor_1ro = CustomUser.objects.create_user(
                email='preceptor1ro@secundaria.edu',
                password='password',
                first_name='Andrea',
                last_name='Quiroga',
                gender='femenino',
                document='26789022',
                profile_picture=defaultuser,
                hoursToWork=20,
                phone='3516701200',
                documentType=dni,
                nationality=argentina,
                contactInfo=contact_info_preceptor_1ro,
                email_verified=True
            )