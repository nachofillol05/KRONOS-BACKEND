# Módulos Lasalle
modules_lasalle = []
for i, day in enumerate(days_of_week, start=1):
    for j in range(1, 6):
        module_lasalle = Module.objects.create(
            moduleNumber=j,
            day=day,
            startTime=time(9 + j, 0),
            endTime=time(10 + j, 0),
            school=school_lasalle
        )
        modules_lasalle.append(module_lasalle)