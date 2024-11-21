from django.core.management.base import BaseCommand
from Kronosapp.management.seeds.core.DocumentType import seed_DocumentType
from Kronosapp.management.seeds.core.Nationality import seed_Nationality
from Kronosapp.management.seeds.schools.test import test_seed

class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_DocumentType()
        seed_Nationality()

        test_seed()

