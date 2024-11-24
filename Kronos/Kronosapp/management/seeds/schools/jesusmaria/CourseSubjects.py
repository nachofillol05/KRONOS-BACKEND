from Kronosapp.models import CourseSubjects,Course,Subject

def seed_CourseSubject_JM():

    # Sets weekly hours
    weeklyHours = 5
    
    # Imports relevant subjects and courses
    subjectsJM= Subject.objects.filter(school__name='Jesus Maria')
    coursesJM= Course.objects.filter(year__school__name='Jesus Maria')

    # Bulk creation of CourseSubjects
    CourseSubjects.objects.bulk_create(
        CourseSubjects(
            studyPlan=f"Plan de estudio de {subject.name} {course.name}",
            subject=subject,
            course=course,
            weeklyHours=weeklyHours
        )
        for i, subject in enumerate(subjectsJM) # i and j are used to correctly position subject and course by using the enumerate() function
        for j ,course in enumerate(coursesJM)

    )
