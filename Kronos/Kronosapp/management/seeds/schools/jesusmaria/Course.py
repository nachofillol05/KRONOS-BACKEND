from Kronosapp.models import Course
from Kronosapp.management.seeds.schools.jesusmaria.Year import get_years_JM

def seed_Course_JM():
    # List of course names
    course_names = ['A', 'B', 'C']
    
    courses_to_create = []
    yearsJM = get_years_JM()

    # Iterate through each year
    for year in yearsJM:
        # Create courses for each year
        for name in course_names:
            course_name = f"{year.number}°{name}"  # Format the course name (e.g., "1°A")
            course = Course(
                name=course_name,
                year=year
            )
            courses_to_create.append(course)

    # Bulk insert all the created courses into the database
    Course.objects.bulk_create(courses_to_create)

