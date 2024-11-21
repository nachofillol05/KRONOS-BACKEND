# Materias para Lasalle
subjectsLS = []
subject_math_lasalle = Subject.objects.create(
    name="Matemáticas",
    color='#C0392B',  
    abbreviation="MAT",
    school=school_lasalle
)
subjectsLS.append(subject_math_lasalle)

subject_physics_lasalle = Subject.objects.create(
    name="Física",
    color='#2980B9',  
    abbreviation="FIS",
    school=school_lasalle
)
subjectsLS.append(subject_physics_lasalle)