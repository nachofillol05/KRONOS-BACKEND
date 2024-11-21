course_names = ['A', 'B', 'C']
courses_villada = []
for year in [year1_villada, year2_villada, year3_villada, year4_villada, year5_villada, year6_villada, year7_villada]:
    for name in course_names:
        course_name = f"{year.number}°{name}"
        course = Course.objects.create(name=course_name, year=year)
        courses_villada.append(course)