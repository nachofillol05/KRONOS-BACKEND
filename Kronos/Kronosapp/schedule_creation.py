import time
import pulp

from .  utils import convert_binary_to_image
from .models import TeacherSubjectSchool, TeacherAvailability, Course, Module, Schedules



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
    import pulp
    import time

    # Obtener materias dinámicamente
    subjects = get_subjects_dynamically(user_school=user_school)

    # Reducir horarios redundantes
    for subject in subjects:
        subjects[subject]["availability"] = list(set(subjects[subject]["availability"]))

    # Crear lista única de horarios disponibles
    course_schedules = list(set(
        schedule for subject in subjects for schedule in subjects[subject]["availability"]
    ))

    # Variables de decisión
    assignment = pulp.LpVariable.dicts(
        "assignment",
        ((subject, schedule) for subject in subjects for schedule in subjects[subject]["availability"]),
        cat="Binary"
    )

    # Problema de optimización
    problem = pulp.LpProblem("Schedule_Assignment", pulp.LpMaximize)

    # Función objetivo: Maximizar las horas asignadas
    problem += pulp.lpSum(assignment[subject, schedule] 
                          for subject in subjects 
                          for schedule in subjects[subject]["availability"])

    # Restricción 1: Asignar cada materia hasta las horas requeridas
    for subject in subjects:
        problem += pulp.lpSum(assignment[subject, schedule] 
                              for schedule in subjects[subject]["availability"]) <= subjects[subject]["hours"]

    # Restricción 2: Evitar más de una asignación por horario
    for schedule in course_schedules:
        problem += pulp.lpSum(assignment[subject, schedule] 
                              for subject in subjects if schedule in subjects[subject]["availability"]) <= 1

    # Restricción 3: Evitar conflictos de profesores en el mismo bloque horario
    teacher_availability = {}
    for subject in subjects:
        teacher = subjects[subject]["teacher"]
        for schedule in subjects[subject]["availability"]:
            if teacher not in teacher_availability:
                teacher_availability[teacher] = {}
            day_hour = "_".join(schedule.split("_")[:2])
            if day_hour not in teacher_availability[teacher]:
                teacher_availability[teacher][day_hour] = []
            teacher_availability[teacher][day_hour].append((subject, schedule))

    for teacher, day_hours in teacher_availability.items():
        for day_hour, assignments in day_hours.items():
            problem += pulp.lpSum(assignment[subject, schedule] for subject, schedule in assignments) <= 1

    # Resolver el problema
    start_time = time.time()
    solver = pulp.PULP_CBC_CMD(timeLimit=180, msg=True)
    problem.solve(solver)
    elapsed_time = time.time() - start_time
    print(f"Tiempo de ejecución: {elapsed_time} segundos")

    # Evaluar resultados
    unassigned_subjects = {subject: subjects[subject]["hours"] for subject in subjects}
    for subject in subjects:
        for schedule in subjects[subject]["availability"]:
            if pulp.value(assignment[subject, schedule]) == 1:
                unassigned_subjects[subject] -= 1

    # Crear horario vacío
    schedule = {}
    modules = Module.objects.filter(school=user_school)
    assigned_modules = Schedules.objects.filter(tssId__school=user_school).values_list('module', flat=True)
    available_modules = modules.exclude(id__in=assigned_modules)

    for module in available_modules:
        day = module.day.capitalize()
        hour = f"Hour{module.moduleNumber}"
        course_str = module.school.name
        schedule[f"{day}_{hour}_{course_str}"] = None

    # Llenar horario con asignaciones
    for subject in subjects:
        for schedule_key in subjects[subject]["availability"]:
            if pulp.value(assignment[subject, schedule_key]) == 1:
                schedule[schedule_key] = subject

    # Crear lista de errores
    subject_errors = [
        f"La materia {subject} tiene {hours} horas sin asignar"
        for subject, hours in unassigned_subjects.items() if hours > 0 and "freeSubject" not in subject
    ]

    # Crear lista de horarios finales
    schedule_list = []
    for schedule_key, subject in schedule.items():
        if subject is not None:
            day, hour, course_str = schedule_key.split("_")
            tss_id = subjects[subject]["tss_id"]
            school = subjects[subject]["school_id"]
            teacher = subjects[subject]["teacher_class"]
            course_obj = Course.objects.get(name=course_str, year__school=school)
            profile_picture_base64 = None

            if teacher.profile_picture:
                profile_picture_base64 = convert_binary_to_image(teacher.profile_picture)

            schedule_list.append({
                "subject_id": subjects[subject]["subject"].id,
                "subject_color": subjects[subject]["subject"].color,
                "subject_name": subjects[subject]["subject"].name,
                "subject_abreviation": subjects[subject]["subject"].abbreviation,
                "name": f"{teacher.first_name} {teacher.last_name}",
                "teacher_id": teacher.id,
                "day": day,
                "moduleNumber": int(hour.replace("Hour", "")),
                "course": course_str,
                "profile_picture": profile_picture_base64,
                "course_id": course_obj.id,
                "tss_id": tss_id,
                "school_id": school,
            })

    return [schedule_list, subject_errors]
