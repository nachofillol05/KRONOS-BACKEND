from Kronosapp.models import Course
from Year import yearsJM

def seed_Course_JM():
    # Crear Curso
    course_names = ['A', 'B', 'C']

    # Crear cursos para los años de Jesús María
    coursesJM = []
    for year in yearsJM:
        for name in course_names:
            course_name = f"{year.number}°{name}"
            course = Course.objects.create(name=course_name, year=year)
            coursesJM.append(course)

