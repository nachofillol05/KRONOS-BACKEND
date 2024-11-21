from Kronosapp.models import Module,School
from datetime import time

def seed_Module_JM():

    school = School.objects.get(name='Jesus Maria')# Defines which school
         
    # Creation of some variables
    days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']
    modules_list = []
    max_daily_modules = 6

    # Iterate through each day of the week
    for day in days_of_week:
        # Create 5 modules (one for each time slot per day)
        for module_number in range(1, max_daily_modules):
            # Create a new module for each day and timeslot
            module = Module(
                moduleNumber=module_number,  # Set module number (1-5)
                day=day,  # Day of the week (e.g., lunes, martes, etc.)
                startTime=time(8 + module_number, 0),  # Starting time (8:00 + module number)
                endTime=time(9 + module_number, 0),  # Ending time (9:00 + module number)
                school=school  # The associated school for the module
            )
            # Append the created module to the list
            modules_list.append(module)

    # Bulk insert all created modules into the database
    Module.objects.bulk_create(modules_list)


    #Comments provided by ChatGPT

