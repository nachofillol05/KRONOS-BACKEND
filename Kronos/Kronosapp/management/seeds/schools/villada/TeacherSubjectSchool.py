subject_per_teacher = 12
# TSS Villada
for i, coursesubject in enumerate(coursesubjectV):
    # Determinar el profesor actual usando división entera
    teacher = teacherV[(i // subject_per_teacher) % len(teacherV)]
    TeacherSubjectSchool.objects.create(
        school=school_villada,
        coursesubjects=coursesubject,
        teacher=teacher
    )