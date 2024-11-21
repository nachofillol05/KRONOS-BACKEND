# Crear escuela Villada
school_villada = School.objects.create(
    name='Villada',
    abbreviation='VIL',
    logo=defaultuser,  # Define este logotipo en seed_images.py
    email='contacto@villada.edu',
    contactInfo=contact_info_villada
)
