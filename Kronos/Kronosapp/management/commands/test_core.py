from typing import Any
from django.core.management.base import BaseCommand
from Kronosapp.management.seeds.core.Action import seed_Action
from Kronosapp.management.seeds.core.AvailabilityState import seed_AvailabilityState
from Kronosapp.management.seeds.core.DocumentType import seed_DocumentType
from Kronosapp.management.seeds.core.EventType import seed_EventType
from Kronosapp.management.seeds.core.Nationality import seed_Nationality
from Kronosapp.management.seeds.core.Role import seed_Role

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        seed_Action()
        seed_AvailabilityState()
        seed_DocumentType()
        seed_EventType()
        seed_Nationality()
        seed_Role()
        