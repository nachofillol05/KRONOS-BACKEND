from Kronosapp.models import TeacherSubjectSchool,CourseSubjects,CustomUser,School

def seed_TeacherSubjectSchool_JM():

    school = School.objects.get(name='Jesus Maria')
    
    coursesubjectJM = CourseSubjects.objects.filter(course__year__school__name='Jesus Maria')

    users = CustomUser.objects.all()
    teachers = []
    for i, user in enumerate(users):
        if i >= 6 and i <= 18:
            teachers.append(user)

    # Asignar profesor a materia en una escuela
    subjects_per_teacher = 12
    # TSS JM
    for i, coursesubject in enumerate(coursesubjectJM):
        # Determinar el profesor actual usando división entera
        teacher = teachers[(i // subjects_per_teacher) % len(teachers)]
        TeacherSubjectSchool.objects.create(
            school=school,
            coursesubjects=coursesubject,
            teacher=teacher
        )