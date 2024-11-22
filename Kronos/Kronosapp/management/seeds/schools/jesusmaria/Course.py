from Kronosapp.models import Course,Year

def seed_Course_JM():
    # Imports relevant years
    yearsJM = Year.objects.filter(school__name='Jesus Maria')
    # Defines the names of the courses
    course_names = ['A', 'B', 'C'] 

    # Bulk creation of courses
    Course.objects.bulk_create(
        Course(
            name=f"{year.number}°{name}",# Formats the name of the course [X° X] e.g.: 1°A
            year=year
        )
        for year in yearsJM
        for name in course_names
    )