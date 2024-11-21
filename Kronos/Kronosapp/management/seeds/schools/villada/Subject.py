subjectsV = []
subject_math_villada = Subject.objects.create(
    name="Matemáticas",
    color='#C0392B',  
    abbreviation="MAT",
    school=school_villada
)
subjectsV.append(subject_math_villada)

subject_physics_villada = Subject.objects.create(
    name="Física",
    color='#2980B9',  
    abbreviation="FIS",
    school=school_villada
)
subjectsV.append(subject_physics_villada)
