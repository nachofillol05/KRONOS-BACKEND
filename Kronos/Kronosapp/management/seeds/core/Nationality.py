from Kronosapp.models import Nationality

def seed_Nationality():
    # Defines nationalities to create
    nationalities = [
        {"name": "Argentina", "description": "Nacionalidad argentina"},
        {"name": "Uruguay", "description": "Nacionalidad uruguaya"},
        {"name": "Brasil", "description": "Nacionalidad brasileña"},
        {"name": "Paraguay", "description": "Nacionalidad paraguaya"},
        {"name": "Chile", "description": "Nacionalidad chilena"},
        {"name": "Bolivia", "description": "Nacionalidad boliviana"},
        {"name": "Perú", "description": "Nacionalidad peruana"},
        {"name": "Otros", "description": "Nacionalidad otros"},
    ]

    # Bulk creation of nationalities
    Nationality.objects.bulk_create(
        [Nationality(name=n["name"], description=n["description"]) for n in nationalities]
    )
