from Kronosapp.models import Event,School,EventType
from django.utils import timezone
from datetime import timedelta

def seed_Event_JM():

    school = School.objects.get(name='Jesus Maria')# Defines which school

    paroDeTransporte = EventType.objects.get(name="Paro de transporte")
    paroDocente = EventType.objects.get(name="Paro docente")
    tallerDocente = EventType.objects.get(name="Taller docente")
    mantenimiento= EventType.objects.get(name="Mantenimiento infraestructura")
    viajeEscolar = EventType.objects.get(name="Viaje escolar")
    otro = EventType.objects.get(name="Otro")

    # Define the events to be created
    events_list = [
        {
            'name': 'Paro general de transporte',
            'startDate': timezone.now(),
            'endDate': timezone.now() + timedelta(days=1),
            'eventType': paroDeTransporte
        },
        {
            'name': 'Excursión al museo de ciencias',
            'startDate': timezone.now() + timedelta(days=1),
            'endDate': timezone.now() + timedelta(days=0, hours=6),
            'eventType': viajeEscolar
        },
        {
            'name': 'Paro docente provincial',
            'startDate': timezone.now() + timedelta(days=7),
            'endDate': timezone.now() + timedelta(days=7, hours=10),
            'eventType': paroDocente
        },
        {
            'name': 'Taller docente de actualización pedagógica',
            'startDate': timezone.now() + timedelta(days=10),
            'endDate': timezone.now() + timedelta(days=10, hours=4),
            'eventType': tallerDocente
        },
        {
            'name': 'Fumigacion',
            'startDate': timezone.now() + timedelta(days=7),
            'endDate': timezone.now() + timedelta(days=7, hours=4),
            'eventType': mantenimiento
        },
        {
            'name': 'Capacitación en tecnologías educativas',
            'startDate': timezone.now() + timedelta(days=15),
            'endDate': timezone.now() + timedelta(days=15, hours=8),
            'eventType': tallerDocente
        },
        {
            'name': 'Día de puertas abiertas',
            'startDate': timezone.now() + timedelta(days=20),
            'endDate': timezone.now() + timedelta(days=20, hours=6),
            'eventType': otro
        },
        {
            'name': 'Simulacro de evacuación',
            'startDate': timezone.now() + timedelta(days=3),
            'endDate': timezone.now() + timedelta(days=3, hours=1),
            'eventType': otro
        },
        {
            'name': 'Charlas sobre educación ambiental',
            'startDate': timezone.now() + timedelta(days=5),
            'endDate': timezone.now() + timedelta(days=5, hours=3),
            'eventType': viajeEscolar
        },
        {
            'name': 'Jornada de salud y bienestar',
            'startDate': timezone.now() + timedelta(days=12),
            'endDate': timezone.now() + timedelta(days=12, hours=4),
            'eventType': otro
        },
        {
            'name': 'Feria del libro escolar',
            'startDate': timezone.now() + timedelta(days=25),
            'endDate': timezone.now() + timedelta(days=26),
            'eventType': viajeEscolar
        },
        {
            'name': 'Competencia deportiva interescolar',
            'startDate': timezone.now() + timedelta(days=26),
            'endDate': timezone.now() + timedelta(days=27, hours=5),
            'eventType': viajeEscolar
        },
        {
            'name': 'Semana de actividades culturales',
            'startDate': timezone.now() + timedelta(days=30),
            'endDate': timezone.now() + timedelta(days=34, hours=12),
            'eventType': otro
        },
        {
            'name': 'Capacitación en primeros auxilios',
            'startDate': timezone.now() + timedelta(days=10),
            'endDate': timezone.now() + timedelta(days=10, hours=3),
            'eventType': viajeEscolar
        }
    ]

    # Bulk creation of events
    Event.objects.bulk_create(
        [Event(name=event["name"],startDate=event["startDate"],endDate=event["endDate"],school=school,eventType=event["eventType"])
               for event in events_list]
    )
