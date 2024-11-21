# Crear Curso
course_names = ['A', 'B', 'C']

# Crear cursos para los años de Jesús María
coursesJM = []
for year in [year1, year2, year3, year4, year5, year6]:
    for name in course_names:
        course_name = f"{year.number}°{name}"
        course = Course.objects.create(name=course_name, year=year)
        coursesJM.append(course)

