for j, teacher in enumerate(teacherV):
    for i, module in enumerate(modulesVillada):
        availabilityState = available if i % 3 < 2 else not_available
        TeacherAvailability.objects.create(
            module=module,
            teacher=teacher,
            loadDate=datetime.now(),
            availabilityState=availabilityState
        )