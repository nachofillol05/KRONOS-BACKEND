for j, teacher in (teacherLS):
    for i, module in (modules_lasalle):
        availabilityState = available if i % 3 < 2 else not_available
        TeacherAvailability.objects.create(
            module=module,
            teacher=teacher,
            loadDate=datetime.now(),
            availabilityState=availabilityState
        )