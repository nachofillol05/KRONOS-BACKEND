# Crear cursos para Lasalle
courses_lasalle = []
for year in [year1_lasalle, year2_lasalle, year3_lasalle, year4_lasalle, year5_lasalle, year6_lasalle]:
    for name in course_names:
        course_name = f"{year.number}°{name}"
        course = Course.objects.create(name=course_name, year=year)
        courses_lasalle.append(course)
