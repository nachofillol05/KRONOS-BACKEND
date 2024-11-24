from datetime import datetime
from Kronosapp.models import TeacherAvailability,CustomUser,Module,AvailabilityState

def seed_TeacherAvailability_JM():

    available = AvailabilityState.objects.get(name="Disponible")
    not_available = AvailabilityState.objects.get(name="No Disponible")

    modules = Module.objects.filter(school__name='Jesus Maria')
    users = CustomUser.objects.all()
    
    teachers = []
    for i, user in enumerate(users):
        if i >= 6 and i <= 18:
            teachers.append(user)

    TeacherAvailability.objects.bulk_create(
        TeacherAvailability(
            module=module,
            teacher=teacher,
            loadDate=datetime.now(),
            availabilityState=(available if i % 3 < 2 else not_available)
        )
        for teacher in teachers
        for i, module in enumerate(modules)
    )