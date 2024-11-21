# Asignar profesor a materia en una escuela
subjects_per_teacher = 12
# TSS JM
for i, coursesubject in enumerate(coursesubjectJM):
    # Determinar el profesor actual usando división entera
    teacher = teacherJM[(i // subjects_per_teacher) % len(teacherJM)]
    TeacherSubjectSchool.objects.create(
        school=school,
        coursesubjects=coursesubject,
        teacher=teacher
    )