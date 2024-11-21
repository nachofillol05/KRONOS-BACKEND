coursesubjectsV = []
for subject in enumerate(subjectsV):
    for course in enumerate(coursesV):
        studyPlan = f"Plan de estudio de {subject.name} {course.name}"
        coursesubject = CourseSubjects.objects.create(
            studyPlan=studyPlan, 
            subject=subject, 
            course=course, 
            weeklyHours=5
        )
        coursesubjectsV.append(coursesubject)
