from Kronosapp.models import Module
from datetime import time

def seed_Module():
    # Defines modules to create

    # Bulk creation of modules


    
    # Crear módulos
    days_of_week = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']
    modulesJM = []
    for i, day in enumerate(days_of_week, start=1):
        for j in range(1, 6):
            module = Module.objects.create(
                moduleNumber=j,
                day=day,
                startTime=time(8 + j, 0),
                endTime=time(9 + j, 0),
                school=school
            )
            modulesJM.append(module)