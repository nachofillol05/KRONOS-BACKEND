from Kronosapp.models import Year, School

def seed_year_JM():

    school = School.objects.get(name='Jesus Maria')# Defines which school
    
    # Defines years to create
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

    # Bulk create years
    Year.objects.bulk_create(yearsJM)
