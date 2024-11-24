from django.core.management.base import BaseCommand
from Kronosapp.management.seeds.schools.test import test_seed
from Kronosapp.management.seeds.schools.jesusmaria.ContactInformation import seed_ContactInformation_JM
from Kronosapp.management.seeds.schools.jesusmaria.School import seed_School_JM
from Kronosapp.management.seeds.schools.jesusmaria.Year import seed_year_JM
from Kronosapp.management.seeds.schools.jesusmaria.Subject import seed_Subject_JM
from Kronosapp.management.seeds.schools.jesusmaria.Module import seed_Module_JM
from Kronosapp.management.seeds.schools.jesusmaria.Course import seed_Course_JM
from Kronosapp.management.seeds.schools.jesusmaria.Event import seed_Event_JM
from Kronosapp.management.seeds.schools.jesusmaria.CustomUser import seed_CustomUser_JM
from Kronosapp.management.seeds.schools.jesusmaria.CourseSubjects import seed_CourseSubject_JM
from Kronosapp.management.seeds.schools.jesusmaria.TeacherAvailability import seed_TeacherAvailability_JM
from Kronosapp.management.seeds.schools.jesusmaria.TeacherSubjectSchool import seed_TeacherSubjectSchool_JM

from Kronosapp.models import Year

class Command(BaseCommand):
    def handle(self, *args, **options):

        
        seed_ContactInformation_JM()
        print("seed_ContactInformation_JM")

        seed_School_JM()
        print("seed_School_JM")
        
        seed_Subject_JM()
        print("seed_Subject_JM")
        
        seed_Module_JM()
        print("seed_Module_JM")

        seed_Event_JM()
        print("seed_Event_JM")

        seed_year_JM()
        print("seed_year_JM")

        seed_Course_JM()
        print("seed_Course_JM")
        
        seed_CustomUser_JM()
        print("seed_CustomUser_JM")

        seed_CourseSubject_JM()
        print("seed_CourseSubjects_JM")

        seed_TeacherAvailability_JM()
        print("seed_TeacherAvailability_JM")

        seed_TeacherSubjectSchool_JM()
        print("seed_TeacherSubjectSchool_JM")
        
        

        