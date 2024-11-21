#Order 1
from Kronosapp.models import ContactInformation

def seed_ContactInformation_JM():
    # Defines contact information to create
    contact_info_list = [
        # Directive
        {
            "postalCode": "5000",
            "street": "Calle Nash", "streetNumber": "294",
            "city": "Córdoba", "province": "Córdoba"
        },
        # Teachers
        {
            "postalCode": "5001",
            "street": "Calle San Jerónimo", "streetNumber": "101",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5002",
            "street": "Calle Obispo Trejo", "streetNumber": "102",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5003",
            "street": "Calle Vélez Sarsfield", "streetNumber": "103",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5004",
            "street": "Calle 9 de Julio", "streetNumber": "104",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5005",
            "street": "Avenida Olmos", "streetNumber": "105",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5006",
            "street": "Avenida General Paz", "streetNumber": "106",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5007",
            "street": "Calle Ituzaingó", "streetNumber": "107",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5008",
            "street": "Calle Tucumán", "streetNumber": "108",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5009",
            "street": "Avenida Maipú", "streetNumber": "109",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5010",
            "street": "Calle Belgrano", "streetNumber": "110",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5025",
            "street": "Avenida del Trabajo", "streetNumber": "250",
            "city": "Córdoba", "province": "Córdoba"
        },
        # Preceptores
        {
            "postalCode": "5000",
            "street": "Avenida Colón", "streetNumber": "2345",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5000",
            "street": "Calle Duarte Quiros", "streetNumber": "3456",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5000",
            "street": "Calle La Rioja", "streetNumber": "4567",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5000",
            "street": "Calle Catamarca", "streetNumber": "5678",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5000",
            "street": "Calle Mendoza", "streetNumber": "6789",
            "city": "Córdoba", "province": "Córdoba"
        },
        {
            "postalCode": "5000",
            "street": "Calle Entre Ríos", "streetNumber": "7890",
            "city": "Córdoba", "province": "Córdoba"
        },
        # School
        {
            "postalCode": "4000",
            "street": "Calle San Martín", "streetNumber": "101",
            "city": "San Miguel de Tucumán", "province": "Tucumán"
        }
    ]

    # Bulk creation of contact information
    ContactInformation.objects.bulk_create(
        [ContactInformation(
            postalCode=contact["postalCode"],
            street=contact["street"], streetNumber=contact["streetNumber"],
            city=contact["city"], province=contact["province"]
        ) for contact in contact_info_list]
    )