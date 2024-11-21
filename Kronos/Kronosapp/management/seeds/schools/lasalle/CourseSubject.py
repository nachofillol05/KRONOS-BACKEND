# Asignar materias a cursos en Lasalle
coursesubjectsLS = []
for subject in enumerate(subjectsLS):
    for course in enumerate(coursesLS):
        studyPlan = f"Plan de estudio de {subject.name} {course.name}"
        coursesubject = CourseSubjects.objects.create(
            studyPlan=studyPlan, 
            subject=subject, 
            course=course, 
            weeklyHours=5
        )
        coursesubjectsLS.append(coursesubject)
