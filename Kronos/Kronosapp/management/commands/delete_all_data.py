from django.core.management.base import BaseCommand

from django.db import connection #Allows direct interaction with the database via the use of regular MySQL sintax.

from Kronosapp.models import (
    DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event, Role, CourseSubjects #WHEN ADDING A MODEL HERE, ALSO ADD IT TO 'selected_kronosapp_models' BELOW
    )

selected_kronosapp_models = [DocumentType, Nationality, ContactInformation, School,
    CustomUser, Module, AvailabilityState, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Action,
    EventType, Event, Role, CourseSubjects # <------ HERE
    ]

class Command(BaseCommand):
    help = 'Delete all data from the database'
    # python manage.py delete_all_data
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            self.stdout.write(self.style.WARNING('Initializing data deletion...'))

            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;') #Prevents constraint violations temporarily
            
            #Automatically fetches all KronosApp models currently imported
            self.stdout.write(self.style.WARNING('Importing tables...'))
            tables = [model._meta.db_table for model in selected_kronosapp_models]
            
            # Truncate (delete) tables and reset AUTO_INCREMENT
            modelsCount = len(selected_kronosapp_models)
            for i,table in enumerate(tables, start=1):
                self.stdout.write(self.style.WARNING(f'Deleting table {table}...({i}/{modelsCount})'))
                cursor.execute(f'TRUNCATE TABLE `{table}`;')
            
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

        self.stdout.write(self.style.SUCCESS('\nAll data has been successfuly deleted from the database.\n'))
