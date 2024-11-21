from django.core.management.base import BaseCommand
from Kronosapp.management.seeds.schools.test import test_seed
from Kronosapp.management.seeds.schools.jesusmaria.ContactInformation import seed_ContactInformation_JM
from Kronosapp.management.seeds.schools.jesusmaria.School import seed_School_JM
from Kronosapp.management.seeds.schools.jesusmaria.Year import seed_year_JM
from Kronosapp.management.seeds.schools.jesusmaria.Subject import seed_Subject_JM
from Kronosapp.management.seeds.schools.jesusmaria.Module import seed_Module_JM

class Command(BaseCommand):
    def handle(self, *args, **options):

        seed_ContactInformation_JM()
        seed_School_JM()
        seed_Subject_JM()
        seed_Module_JM()
        seed_year_JM()

        