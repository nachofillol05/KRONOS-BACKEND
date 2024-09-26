import time
import pulp

from .  utils import convert_binary_to_image
from .models import TeacherSubjectSchool, TeacherAvailability, Course, Module



def get_subjects_dynamically(user_school):
    subjects = {}

    tss_records = TeacherSubjectSchool.objects.filter(coursesubjects__isnull=False, school=user_school)

    for tss in tss_records:
        tss_id = tss.id
        subject = tss.coursesubjects.subject
        weeklyHours = tss.coursesubjects.weeklyHours
        teacher = tss.teacher
        school = tss.school.id
        course = tss.coursesubjects.course

        if course and course.name not in subjects:
            subjects[subject.name, course.name] = {
                "subject": subject,
                "hours": weeklyHours,
                "availability": [],
                "teacher_class": teacher,
                "teacher": f"{teacher.first_name} {teacher.last_name}",
                "tss_id": tss_id,
                "school_id": school
            }

        availability_records = TeacherAvailability.objects.filter(teacher=teacher)
        for availability in availability_records:
            module = availability.module
            day = module.day.capitalize()
            hour = f"Hour{module.moduleNumber}"
            course_str = course.name

            availability_str = f"{day}_{hour}_{course_str}"
            subjects[subject.name, course.name]["availability"].append(availability_str)

    return subjects


def schedule_creation(user_school):
    subjects = get_subjects_dynamically(user_school=user_school)
    
    # Filtrar horarios solo disponibles
    course_schedules = list(set(
        schedule for s in subjects for schedule in subjects[s]["availability"]
    ))

    # Variables de decisión
    assignment = pulp.LpVariable.dicts(
        "assignment",
        ((subject, course_schedule) for subject in subjects for course_schedule in subjects[subject]["availability"]),
        cat="Binary"
    )

    # Problema de optimización
    problem = pulp.LpProblem("Schedule_Assignment", pulp.LpMaximize)

    # Función objetivo: maximizar las horas asignadas
    problem += pulp.lpSum(assignment[subject, course_schedule] for subject in subjects for course_schedule in subjects[subject]["availability"])

    # Restricciones
    for subject in subjects:
        problem += pulp.lpSum(assignment[subject, course_schedule] for course_schedule in subjects[subject]["availability"]) <= subjects[subject]["hours"]

    for course_schedule in course_schedules:
        problem += pulp.lpSum(assignment[subject, course_schedule] for subject in subjects if course_schedule in subjects[subject]["availability"]) <= 1

    for course_schedule in course_schedules:
        day_hour = "_".join(course_schedule.split("_")[:2])
        for subject1 in subjects:
            for subject2 in subjects:
                if subject1 != subject2 and subjects[subject1]["teacher"] == subjects[subject2]["teacher"]:
                    avail1 = [s for s in subjects[subject1]["availability"] if day_hour in s]
                    avail2 = [s for s in subjects[subject2]["availability"] if day_hour in s]
                    if avail1 and avail2:
                        problem += pulp.lpSum(assignment[subject1, s] for s in avail1) + pulp.lpSum(assignment[subject2, s] for s in avail2) <= 1

    # Establecer el límite de tiempo del solver a 2 minutos (120 segundos)
    start_time = time.time()

    solver = pulp.PULP_CBC_CMD(timeLimit=180)
    problem.solve(solver)

    elapsed_time = time.time() - start_time
    print(f"Tiempo de ejecución: {elapsed_time} segundos")

    # Guardar los resultados
    unassigned_subjects = {subject: subjects[subject]["hours"] for subject in subjects}
    for subject in subjects:
        for course_schedule in subjects[subject]["availability"]:
            if pulp.value(assignment[subject, course_schedule]) == 1:
                unassigned_subjects[subject] -= 1

    # Creación de horario vacío
    schedule = {}
    modules = Module.objects.filter(school=user_school)
    assigned_modules = Schedules.objects.filter(tssId__school=user_school).values_list('module', flat=True)
    available_modules = modules.exclude(id__in=assigned_modules)

    # Actualizar las horas asignadas para cada materia (subject)
    for subject in subjects:
        # Filtramos los módulos de disponibilidad de la materia
        assigned_count = 0
        for assigned_module in assigned_modules:
            if assigned_module in subjects[subject]["availability"]:
                assigned_count += 1
        # Restar la cantidad correspondiente de horas asignadas
        subjects[subject]["hours"] -= assigned_count

    # Crear los módulos disponibles
    for module in available_modules:
        day = module.day.capitalize()
        hour = f"Hour{module.moduleNumber}"
        course_str = module.school.name 

        schedule[f"{day}_{hour}_{course_str}"] = None

    for subject in subjects:
        for course_schedule in subjects[subject]["availability"]:
            if pulp.value(assignment[subject, course_schedule]) == 1:
                schedule[course_schedule] = subject

    # Mostrar los errores de asignación
    subject_errors = []
    for subject, remaining_hours in unassigned_subjects.items():
        if remaining_hours > 0:
            subject_errors.append(f"La materia {subject} tiene {remaining_hours} horas sin asignar")

    # Crear la lista final de horarios
    schedule_list = []
    for course_schedule, subject in schedule.items():
        if subject is not None:
            day, hour, course_str = course_schedule.split("_")
            tss_id = subjects[subject]["tss_id"]
            school = subjects[subject]["school_id"]
            

            # Extraer solo los campos serializables del profesor (teacher)
            teacher = subjects[subject]["teacher_class"]
            teacher_name = f"{teacher.first_name} {teacher.last_name}"  # serializar solo el nombre
            teacher_id = teacher.id  # También podrías usar el ID del profesor

            subjectt = subjects[subject]["subject"]
            course_obj = Course.objects.get(name=course_str, year__school=school)
            course_id = course_obj.id
            
            profile_picture_base64 = None
            if teacher.profile_picture:
                profile_picture_base64 = convert_binary_to_image(teacher.profile_picture)
           
            schedule_list.append({
                "subject_id": subjectt.id,
                "subject_color": subjectt.color,
                "subject_name": subjectt.name,
                "subject_abreviation": subjectt.abbreviation,
                "name": teacher_name,  # Nombre del profesor como string
                "teacher_id": teacher_id,  # ID del profesor
                "day": day,
                "moduleNumber": int(hour.replace("Hour", "")),
                "course": course_str,
                "profile_picture": profile_picture_base64,
                "course_id": course_id,
                "tss_id": tss_id,
                "school_id": school
            })

    result = [schedule_list, subject_errors]
    return result
