from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event, Role
)

class Command(BaseCommand):
    help = 'Delete all data from the database'
    # python manage.py delete_all_data
    def handle(self, *args, **options):
        # Eliminar datos de las tablas
        Event.objects.all().delete()
        EventType.objects.all().delete()
        TeacherSubjectSchool.objects.all().delete()
        Subject.objects.all().delete()
        Course.objects.all().delete()
        Year.objects.all().delete()
        TeacherAvailability.objects.all().delete()
        AvailabilityState.objects.all().delete()
        Module.objects.all().delete()
        School.objects.all().delete()
        #CustomUser.objects.all().delete()
        ContactInformation.objects.all().delete()
        Nationality.objects.all().delete()
        DocumentType.objects.all().delete()
        Action.objects.all().delete()
        Role.objects.all().delete()

        CustomUser.objects.filter(is_staff=False, is_superuser=False).delete()

        self.stdout.write(self.style.SUCCESS('All data has been deleted from the database.'))
