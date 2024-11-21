  # Crear escuela Lasalle
school_lasalle = School.objects.create(
    name='Lasalle',
    abbreviation='LAS',
    logo=defaultuser,  # Define este logotipo en seed_images.py
    email='contacto@lasalle.edu',
    contactInfo=contact_info_lasalle
)