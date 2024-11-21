from django.core.management.base import BaseCommand
from Kronosapp.models import (
    DocumentType, Nationality, AvailabilityState, EventType, Role, Action,
    
    ContactInformation, School, CustomUser, Module, TeacherAvailability,
    Year, Course, Subject, TeacherSubjectSchool, Event, CourseSubjects
)

import uuid
from django.utils import timezone
from datetime import time, timedelta, datetime
class Command(BaseCommand):
    help = 'Seed database with initial data'
    # python manage.py seed
    def handle(self, *args, **options):
        print()

       




      

        



        
        
        

        

        