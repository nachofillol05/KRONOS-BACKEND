from Kronosapp.models import Role

def seed_Role():
    # Defines roles to create
    roles = [
        {"name": "Directivo"},
        {"name": "Profesor"},
        {"name": "Preceptor"}
    ]

    # Bulk creation of roles
    Role.objects.bulk_create(
        [Role(name=role["name"]) for role in roles]
    )