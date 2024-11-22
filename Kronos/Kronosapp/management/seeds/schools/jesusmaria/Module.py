from Kronosapp.models import Module,School
from datetime import time

def seed_Module_JM():

    school = School.objects.get(name='Jesus Maria')# Defines which school
         
    # Creation of some variables
    days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']
    max_daily_modules = 5

    Module.objects.bulk_create(
        Module(
            moduleNumber=module_number,  # Set module number (1-5)
            day=day,  # Day of the week (e.g., lunes, martes, etc.)
            startTime=time(8 + module_number, 0),  # Starting time (8:00 + module number)
            endTime=time(9 + module_number, 0),  # Ending time (9:00 + module number)
            school=school  # The associated school for the module
        )
        for day in days_of_week
        for module_number in range(1, max_daily_modules+1)
    )

    #Comments provided by ChatGPT

