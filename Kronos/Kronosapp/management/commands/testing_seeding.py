from django.core.management.base import BaseCommand
from Kronosapp.management.seeds.schools.test import test_seed
from Kronosapp.management.seeds.schools.jesusmaria.ContactInformation import seed_ContactInformation_JM
from Kronosapp.management.seeds.schools.jesusmaria.School import seed_School_JM
from Kronosapp.management.seeds.schools.jesusmaria.Year import seed_year_JM
from Kronosapp.management.seeds.schools.jesusmaria.Subject import seed_Subject_JM
from Kronosapp.management.seeds.schools.jesusmaria.Module import seed_Module_JM
from Kronosapp.management.seeds.schools.jesusmaria.Course import seed_Course_JM

class Command(BaseCommand):
    def handle(self, *args, **options):

        print("1")
        seed_ContactInformation_JM()
        print("2")
        seed_School_JM()
        print("3")
        seed_Subject_JM()
        print("4")
        seed_Module_JM()
        print("5")
        seed_year_JM()
        print("6")
        seed_Course_JM()
        print("7")
        

        