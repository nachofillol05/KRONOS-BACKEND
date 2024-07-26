import pulp
from .models import TeacherSubjectSchool, Subject, TeacherAvailability, CustomUser, Course

def obtener_materias_dinamicamente():
    materias = {}

    # Obtener todos los registros de TeacherSubjectSchool
    tss_records = TeacherSubjectSchool.objects.all()

    for tss in tss_records:
        tss_id = tss.id
        subject = tss.subject
        teacher = tss.teacher
        school = tss.school.id
        course = subject.course

        if course and course.name not in materias:
            materias[subject.name, course.name] = {
                "horas": subject.weeklyHours,
                "disponibilidad": [],
                "profesor": f"{teacher.first_name} {teacher.last_name}",
                "tss_id": tss_id,
                "school_id": school
            }

        # Obtener la disponibilidad del profesor
        availability_records = TeacherAvailability.objects.filter(teacher=teacher)

        for availability in availability_records:
            module = availability.module
            day = module.day.capitalize()
            hour = f"Hora{module.moduleNumber}"
            course_str = f"Curso{course.name}"

            disponibilidad_str = f"{day}_{hour}_{course_str}"
            materias[subject.name, course.name]["disponibilidad"].append(disponibilidad_str)

    return materias


def schedule_creation():
    # Llamar a la función para obtener las materias de manera dinámica
    materias = obtener_materias_dinamicamente()




    # Extraer todos los horarios disponibles puede ser omitido y directamente usar materias[materia]["disponibilidad"]
    horarios_cursos = list(set(horario for m in materias for horario in materias[m]["disponibilidad"]))


    # Variables de decisión
    asignacion = pulp.LpVariable.dicts(
        "asignacion",
        ((materia, horario_curso) for materia in materias for horario_curso in horarios_cursos),
        cat="Binary"
    )


    # Problema de optimización
    problema = pulp.LpProblem("Asignacion_Horarios", pulp.LpMaximize)

    # Función objetivo (maximizar la cantidad de horas asignadas)
    problema += pulp.lpSum(asignacion[materia, horario_curso] for materia in materias for horario_curso in horarios_cursos)
    #se fija que la suma de las asignaciones de las materias en los horarios sea la mayor posible

    # Restricciones

    # 1. Cada materia se debe impartir el número requerido de horas.
    for materia in materias:
        problema += pulp.lpSum(asignacion[materia, horario_curso] for horario_curso in horarios_cursos) <= materias[materia]["horas"]
        

    # 2. Una materia solo puede ser impartida en los horarios disponibles.
    for materia in materias:
        for horario_curso in horarios_cursos:
            if horario_curso not in materias[materia]["disponibilidad"]:
                problema += asignacion[materia, horario_curso] == 0

    # 3. Un horario no puede estar ocupado por más de una materia en total.
    #una materia no se puede dar en dos cursos a la misma hora
    for horario_curso in horarios_cursos:
        problema += pulp.lpSum(asignacion[materia, horario_curso] for materia in materias) <= 1

    # 4. Si hay dos materias a la misma hora en diferentes cursos, deben ser impartidas por diferentes profesores.
    for horario_curso in horarios_cursos:
        dia_hora = "_".join(horario_curso.split("_")[:2]) #saca el dia y la hora de el horario_curso
        for materia1 in materias:
            for materia2 in materias:
                if materia1 != materia2:
                    disp1 = [h for h in materias[materia1]["disponibilidad"] if dia_hora in h] #se fija que la disponibilidad de la materia 1 este en el actual dia_hora de el horario_curso. ejemplo la disponibilidad tiene muchos y va recorriendo el for y se fija que esa fecha hora se cumpla en los 2 para que sea el mismo horario
                    disp2 = [h for h in materias[materia2]["disponibilidad"] if dia_hora in h]
                    if disp1 and disp2 and materias[materia1]["profesor"] == materias[materia2]["profesor"]:#se fija que ninguno de los dos este vacio y que los profesores sean los mismos
                        problema += pulp.lpSum(asignacion[materia1, h] for h in disp1) + pulp.lpSum(asignacion[materia2, h] for h in disp2) <= 1 #si se cumple la condicion anterior entonces se fija que la suma de las asignaciones de las materias en los horarios sean menor o igual a 1
    #ver ese tema de igual disp1 == disp2
    # Resolver el problema
    print(problema)
    problema.solve()

    # Resultados
    #Guarda los valores de cada materia osea matematica tiene 5 horas para despues irlas restando y ver si quedo alguna sin asignar
    materias_sin_asignar = {materia: materias[materia]["horas"] for materia in materias}
    for materia in materias:
        for horario_curso in horarios_cursos:
            if pulp.value(asignacion[materia, horario_curso]) == 1:
                materias_sin_asignar[materia] -= 1
    # Mostrar resultados
    subject_errors = []
    for materia, horas_restantes in materias_sin_asignar.items():
        if horas_restantes > 0:
            subject_errors.append(f"Materia {materia} le quedaron {horas_restantes} horas sin asignar")
        #else:
            #print(f"Materia {materia} fue completamente asignada")

    """for materia in materias:
        for horario_curso in horarios_cursos:
            if pulp.value(asignacion[materia, horario_curso]) == 1:
                print(f"{materia} se enseñará en {horario_curso}")"""
                
    # Crear horario
    horario = {}
    curso = Course.objects.all()
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    for curso in curso:
        for dia in dias:
            for hora in range(1, 11):
                horario[f"{dia}_{hora}_{curso.name}"] = None

    # Llenar horario con las materias asignadas
    for materia in materias:
        for horario_curso in horarios_cursos:
            if pulp.value(asignacion[materia, horario_curso]) == 1:
                horario[horario_curso] = materia

    # Mostrar horario
    lista_horario = []
    for horario_curso, materia in horario.items():
        if materia is not None:
            dia, hora, curso_str = horario_curso.split("_")
            tss_id = materias[materia]["tss_id"]
            school = materias[materia]["school_id"]
            lista_horario.append({
                "dia": dia,
                "hora": int(hora.replace("Hora", "")),
                "curso": curso_str.replace("Curso", ""),
                "tss_id": tss_id,
                "school_id": school
            })
    result = [lista_horario, subject_errors]
    return result