from Kronosapp.models import Subject, School

def seed_Subject_JM():

    school = School.objects.get(name='Jesus Maria')# Defines which school

    # Defines subjects to create with a structure similar to year_data
    subject_list = [
        {"name": "Matemáticas", "color": "#C0392B", "abbreviation": "MAT"},
        {"name": "Física", "color": "#2980B9", "abbreviation": "FIS"},
        {"name": "Química", "color": "#8E44AD", "abbreviation": "QUI"},
        {"name": "Biología", "color": "#27AE60", "abbreviation": "BIO"},
        {"name": "Inglés", "color": "#CCEFB4", "abbreviation": "ING"},
        {"name": "Educación Física", "color": "#9ED1F9", "abbreviation": "EDF"},
        {"name": "Religión", "color": "#CEB1FC", "abbreviation": "REL"},
        {"name": "Lengua", "color": "#FEEEBC", "abbreviation": "LEN"},
        {"name": "Latín", "color": "#63917D", "abbreviation": "LAT"},
        {"name": "Geografía", "color": "#B7A29C", "abbreviation": "GEO"},
        {"name": "Informatica", "color": "#F39C12", "abbreviation": "INF"}
    ]

    # Create Subject objects from the list of dictionaries
    subjectsJM = [
        Subject(name=subject['name'], color=subject['color'], abbreviation=subject['abbreviation'], school=school)
        for subject in subject_list
    ]

    # Bulk creation of subjects
    Subject.objects.bulk_create(subjectsJM)