from Kronosapp.models import Year, School

def get_years_JM():
    school = School.objects.get(name='Jesus Maria')# Defines which school
    
    # Defines years to manage
    year_data = [
        {"name": "1er Año", "number": "1"},
        {"name": "2do Año", "number": "2"},
        {"name": "3er Año", "number": "3"},
        {"name": "4to Año", "number": "4"},
        {"name": "5to Año", "number": "5"},
        {"name": "6to Año", "number": "6"}
    ]

    # Create Year objects from the list of dictionaries into an array
    yearsJM = [
        Year(name=item['name'], number=item['number'], school=school)
        for item in year_data
    ]

    return yearsJM

def seed_year_JM():

    yearsJM = get_years_JM()

    # Bulk create years
    Year.objects.bulk_create(yearsJM)
