from Kronosapp.models import AvailabilityState

def seed_AvailabilityState():
    # Defines availability states to create
    availability_states = [
        {"name": "Disponible", "isEnabled" :True},
        {"name": "No Disponible", "isEnabled": False},
        {"name": "Asignado", "isEnabled": False}
    ]

    # Bulk creation of availability states
    AvailabilityState.objects.bulk_create(
        [AvailabilityState(name=state["name"],isEnabled=state["isEnabled"])for state in availability_states]
    )