#Order 2
from Kronosapp.models import School,ContactInformation
from Kronosapp.management.commands.seed_images import logojesusmaria

def seed_School_JM():
    # Create school 'Jesus Maria'
    School.objects.create(
        name='Jesús María',
        abbreviation='JM',
        logo= logojesusmaria,
        email='contacto@jesusmaria.edu',
        contactInfo=ContactInformation.objects.get(street="Calle San Martín", streetNumber= "101") #Should be dynamic
    )