# Crear materias JM
subjectsJM = []
subject1 = Subject.objects.create(
    name="Matemáticas",
    color='#C0392B',  
    abbreviation="MAT",
    school=school
)
subjectsJM.append(subject1)

subject2 = Subject.objects.create(
    name="Física",
    color='#2980B9',  
    abbreviation="FIS",
    school=school
)
subjectsJM.append(subject2)

subject3 = Subject.objects.create(
    name="Química",
    color='#8E44AD',  
    abbreviation="QUI",
    school=school
)
subjectsJM.append(subject3)

subject4 = Subject.objects.create(
    name="Biología",
    color='#27AE60',  
    abbreviation="BIO",
    school=school
)
subjectsJM.append(subject4)

subject5 = Subject.objects.create(
    name="Inglés",
    color='#F39C12',  
    abbreviation="ING",
    school=school
)
subjectsJM.append(subject5)

subject6 = Subject.objects.create(
    name="Educación Física",
    color='#F39C12',  
    abbreviation="EDF",
    school=school
)
subjectsJM.append(subject6)

subject7 = Subject.objects.create(
    name="Religión",
    color='#F39C12',  
    abbreviation="REL",
    school=school
)
subjectsJM.append(subject7)

subject8 = Subject.objects.create(
    name="Lengua",
    color='#F39C12',  
    abbreviation="LEN",
    school=school
)
subjectsJM.append(subject8)

subject9 = Subject.objects.create(
    name="Latín",
    color='#F39C12',  
    abbreviation="LAT",
    school=school
)
subjectsJM.append(subject9)

subject10 = Subject.objects.create(
    name="Geografía",
    color='#F39C12',  
    abbreviation="GEO",
    school=school
)
subjectsJM.append(subject10)

subject11 = Subject.objects.create(
    name="Informatica",
    color='#F39C12',  
    abbreviation="INF",
    school=school
)
subjectsJM.append(subject11)
