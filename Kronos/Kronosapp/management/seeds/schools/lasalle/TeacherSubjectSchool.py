
subjects_per_teacher = 12
# TSS LS
for i,coursesubject in enumerate(coursesubjectLS):

    teacher = teacherLS[(i // subjects_per_teacher) % len(teacherLS)]
    TeacherSubjectSchool.objects.create(
        school=school,
        coursesubjects=coursesubject,
        teacher=teacher
    )