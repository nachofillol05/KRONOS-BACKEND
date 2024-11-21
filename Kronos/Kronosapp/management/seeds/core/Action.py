from Kronosapp.models import Action

def seed_Action():
    # Defines actions to create
    actions = [
        {"name": "Agregar materia", "isEnabled": True},
        {"name": "Cambiar materia", "isEnabled": False}
    ]

    # Bulk creation of actions
    Action.objects.bulk_create(
            [Action(name=action["name"], isEnabled=action["isEnabled"]) for action in actions]
    )