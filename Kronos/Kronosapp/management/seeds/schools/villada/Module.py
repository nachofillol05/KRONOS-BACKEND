# Módulos Villada
modules_villada = []
for i, day in enumerate(days_of_week, start=1):
    for j in range(1, 6):
        module_villada = Module.objects.create(
            moduleNumber=j,
            day=day,
            startTime=time(7 + j, 0),
            endTime=time(8 + j, 0),
            school=school_villada
        )
        modules_villada.append(module_villada)
