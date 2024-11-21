from Kronosapp.models import EventType

def seed_EventType():
    # Define event types to create
    event_types = [
        {"name": "Paro de transporte", "description": "Interrupción de servicios de transporte."},
        {"name": "Viaje escolar", "description": "Excursión organizada por la escuela."},
        {"name": "Paro docente", "description": "Paro de docentes."},
        {"name": "Taller docente", "description": "Dictado de taller docente."},
        {"name": "Mantenimiento Infraestructura", "description": "Mantenimiento de la infraestructura del instituto."},
        {"name": "Otro", "description": "Otro tipo de evento."}
    ]

    # Bulk creation of event types
    EventType.objects.bulk_create(
        [EventType(name=type["name"],description=type["description"]) for type in event_types]
    )