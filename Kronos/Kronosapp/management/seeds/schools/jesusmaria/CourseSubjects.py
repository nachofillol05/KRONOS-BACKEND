# Asignar materias a cursos
coursesubjectJM = []
for j, subject in enumerate(subjectsJM):
    for i, course in enumerate(coursesJM):
        studyPlan = f"Plan de estudio de {subject.name} {course.name}"
        coursesubject = CourseSubjects.objects.create(studyPlan=studyPlan, subject=subject, course=course, weeklyHours=5)
        coursesubjectJM.append(coursesubject)
print(len(coursesubjectJM))
