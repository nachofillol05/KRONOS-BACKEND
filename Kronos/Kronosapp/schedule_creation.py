import pulp
from .models import TeacherSubjectSchool, Subject, TeacherAvailability, CustomUser, Course

def get_subjects_dynamically():
    subjects = {}

    # Obtener todos los registros de TeacherSubjectSchool
    tss_records = TeacherSubjectSchool.objects.all()

    for tss in tss_records:
        tss_id = tss.id
        subject = tss.subject
        teacher = tss.teacher
        school = tss.school.id
        course = subject.course

        if course and course.name not in subjects:
            subjects[subject.name, course.name] = {
                "hours": subject.weeklyHours,
                "availability": [],
                "teacher": f"{teacher.first_name} {teacher.last_name}",
                "tss_id": tss_id,
                "school_id": school
            }

        # Obtener la disponibilidad del profesor
        availability_records = TeacherAvailability.objects.filter(teacher=teacher)

        for availability in availability_records:
            module = availability.module
            day = module.day.capitalize()
            hour = f"Hour{module.moduleNumber}"
            course_str = f"Course{course.name}"

            availability_str = f"{day}_{hour}_{course_str}"
            subjects[subject.name, course.name]["availability"].append(availability_str)

    return subjects


def schedule_creation():
    # Llamar a la función para obtener las materias de manera dinámica
    subjects = get_subjects_dynamically()

    # Extraer todos los horarios disponibles puede ser omitido y directamente usar subjects[subject]["availability"]
    course_schedules = list(set(schedule for s in subjects for schedule in subjects[s]["availability"]))

    # Variables de decisión
    assignment = pulp.LpVariable.dicts(
        "assignment",
        ((subject, course_schedule) for subject in subjects for course_schedule in course_schedules),
        cat="Binary"
    )

    # Problema de optimización
    problem = pulp.LpProblem("Schedule_Assignment", pulp.LpMaximize)

    # Función objetivo (maximizar la cantidad de horas asignadas)
    problem += pulp.lpSum(assignment[subject, course_schedule] for subject in subjects for course_schedule in course_schedules)
    #se fija que la suma de las asignaciones de las materias en los horarios sea la mayor posible

    # Restricciones

    # 1. Cada materia se debe impartir el número requerido de horas.
    for subject in subjects:
        problem += pulp.lpSum(assignment[subject, course_schedule] for course_schedule in course_schedules) <= subjects[subject]["hours"]

    # 2. Una materia solo puede ser impartida en los horarios disponibles.
    for subject in subjects:
        for course_schedule in course_schedules:
            if course_schedule not in subjects[subject]["availability"]:
                problem += assignment[subject, course_schedule] == 0

    # 3. Un horario no puede estar ocupado por más de una materia en total.
    #una materia no se puede dar en dos cursos a la misma hora
    for course_schedule in course_schedules:
        problem += pulp.lpSum(assignment[subject, course_schedule] for subject in subjects) <= 1

    # 4. Si hay dos materias a la misma hora en diferentes cursos, deben ser impartidas por diferentes profesores.
    for course_schedule in course_schedules:
        day_hour = "_".join(course_schedule.split("_")[:2]) #saca el dia y la hora de el course_schedule
        for subject1 in subjects:
            for subject2 in subjects:
                if subject1 != subject2:
                    avail1 = [s for s in subjects[subject1]["availability"] if day_hour in s] #se fija que la disponibilidad de la materia 1 este en el actual day_hour de el course_schedule. ejemplo la disponibilidad tiene muchos y va recorriendo el for y se fija que esa fecha hora se cumpla en los 2 para que sea el mismo horario
                    avail2 = [s for s in subjects[subject2]["availability"] if day_hour in s]
                    if avail1 and avail2 and subjects[subject1]["teacher"] == subjects[subject2]["teacher"]:#se fija que ninguno de los dos este vacio y que los profesores sean los mismos
                        problem += pulp.lpSum(assignment[subject1, s] for s in avail1) + pulp.lpSum(assignment[subject2, s] for s in avail2) <= 1 #si se cumple la condicion anterior entonces se fija que la suma de las asignaciones de las materias en los horarios sean menor o igual a 1
    #ver ese tema de igual avail1 == avail2
    # Resolver el problema
    print(problem)
    problem.solve()

    # Resultados
    #Guarda los valores de cada materia osea matematica tiene 5 horas para despues irlas restando y ver si quedo alguna sin asignar
    unassigned_subjects = {subject: subjects[subject]["hours"] for subject in subjects}
    for subject in subjects:
        for course_schedule in course_schedules:
            if pulp.value(assignment[subject, course_schedule]) == 1:
                unassigned_subjects[subject] -= 1
    # Mostrar resultados
    subject_errors = []
    for subject, remaining_hours in unassigned_subjects.items():
        if remaining_hours > 0:
            subject_errors.append(f"Subject {subject} has {remaining_hours} hours unassigned")
        #else:
            #print(f"Materia {materia} fue completamente asignada")


    # Crear horario
    schedule = {}
    courses = Course.objects.all()
    days = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for course in courses:
        for day in days:
            for hour in range(1, 11):
                schedule[f"{day}_{hour}_{course.name}"] = None

    # Llenar horario con las materias asignadas
    for subject in subjects:
        for course_schedule in course_schedules:
            if pulp.value(assignment[subject, course_schedule]) == 1:
                schedule[course_schedule] = subject

    # Mostrar horario
    schedule_list = []
    for course_schedule, subject in schedule.items():
        if subject is not None:
            day, hour, course_str = course_schedule.split("_")
            print(day, hour, course)
            tss_id = subjects[subject]["tss_id"]
            school = subjects[subject]["school_id"]
            schedule_list.append({
                "day": day,
                "hour": int(hour.replace("Hour", "")),
                "course": course_str.replace("Curso", ""),
                "tss_id": tss_id,
                "school_id": school
            })
    result = [schedule_list, subject_errors]
    return result
