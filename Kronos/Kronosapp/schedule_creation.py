import pulp

# Datos de entrada
#caso ideal
"""materias = {
    "Matematica 1A": {
        "horas": 6,
        "disponibilidad": ["Dia3_Hora7_Curso1A","Dia3_Hora8_Curso1A","Dia1_Hora7_Curso1A","Dia1_Hora1_Curso1A", "Dia1_Hora2_Curso1A", "Dia2_Hora1_Curso1A", "Dia2_Hora2_Curso1A", "Dia3_Hora1_Curso1A", "Dia3_Hora2_Curso1A"],
        "profesor": "Profesor1"
    },
    "Fisica 1A": {
        "horas": 5,
        "disponibilidad": ["Dia1_Hora3_Curso1A", "Dia1_Hora4_Curso1A", "Dia2_Hora3_Curso1A", "Dia2_Hora4_Curso1A", "Dia3_Hora3_Curso1A"],
        "profesor": "Profesor2"
    },
    "Quimica 1A": {
        "horas": 4,
        "disponibilidad": ["Dia1_Hora5_Curso1A", "Dia1_Hora6_Curso1A", "Dia2_Hora5_Curso1A", "Dia2_Hora6_Curso1A"],
        "profesor": "Profesor3"
    },
    "Biologia 1A": {
        "horas": 3,
        "disponibilidad": ["Dia3_Hora4_Curso1A", "Dia3_Hora5_Curso1A", "Dia3_Hora6_Curso1A"],
        "profesor": "Profesor4"
    },
    "Historia 1A": {
        "horas": 4,
        "disponibilidad": ["Dia4_Hora1_Curso1A", "Dia4_Hora2_Curso1A", "Dia4_Hora3_Curso1A", "Dia4_Hora4_Curso1A"],
        "profesor": "Profesor5"
    },
    "Geografia 1A": {
        "horas": 3,
        "disponibilidad": ["Dia4_Hora5_Curso1A", "Dia4_Hora6_Curso1A", "Dia5_Hora1_Curso1A"],
        "profesor": "Profesor6"
    },
    "Lengua 1A": {
        "horas": 5,
        "disponibilidad": ["Dia5_Hora2_Curso1A", "Dia5_Hora3_Curso1A", "Dia5_Hora4_Curso1A", "Dia5_Hora5_Curso1A", "Dia5_Hora6_Curso1A"],
        "profesor": "Profesor7"
    },
    "Educacion Fisica 1A": {
        "horas": 3,
        "disponibilidad": ["Dia1_Hora1_Curso1A", "Dia1_Hora2_Curso1A", "Dia1_Hora3_Curso1A", "Dia2_Hora1_Curso1A", "Dia2_Hora2_Curso1A", "Dia3_Hora1_Curso1A", "Dia3_Hora2_Curso1A"],
        "profesor": "Profesor8"
    },
    "Matematica 1B": {
        "horas": 6,
        "disponibilidad": ["Dia1_Hora7_Curso1B","Dia1_Hora1_Curso1B", "Dia1_Hora2_Curso1B", "Dia2_Hora1_Curso1B", "Dia2_Hora2_Curso1B", "Dia3_Hora1_Curso1B", "Dia3_Hora2_Curso1B"],
        "profesor": "Profesor9"
    },
    "Fisica 1B": {
        "horas": 5,
        "disponibilidad": ["Dia5_Hora9_Curso1B","Dia1_Hora3_Curso1B", "Dia1_Hora4_Curso1B", "Dia2_Hora3_Curso1B", "Dia2_Hora4_Curso1B", "Dia3_Hora3_Curso1B"],
        "profesor": "Profesor10"
    },
    "Quimica 1B": {
        "horas": 4,
        "disponibilidad": ["Dia1_Hora5_Curso1B", "Dia1_Hora6_Curso1B", "Dia2_Hora5_Curso1B", "Dia2_Hora6_Curso1B"],
        "profesor": "Profesor11"
    },
    "Biologia 1B": {
        "horas": 3,
        "disponibilidad": ["Dia3_Hora4_Curso1B", "Dia3_Hora5_Curso1B", "Dia3_Hora6_Curso1B"],
        "profesor": "Profesor12"
    },
    "Historia 1B": {
        "horas": 4,
        "disponibilidad": ["Dia4_Hora1_Curso1B", "Dia4_Hora2_Curso1B", "Dia4_Hora3_Curso1B", "Dia4_Hora4_Curso1B"],
        "profesor": "Profesor13"
    },
    "Geografia 1B": {
        "horas": 3,
        "disponibilidad": ["Dia4_Hora5_Curso1B", "Dia4_Hora6_Curso1B", "Dia5_Hora1_Curso1B"],
        "profesor": "Profesor14"
    },
    "Lengua 1B": {
        "horas": 5,
        "disponibilidad": ["Dia5_Hora2_Curso1B", "Dia5_Hora3_Curso1B", "Dia5_Hora4_Curso1B", "Dia5_Hora5_Curso1B", "Dia5_Hora6_Curso1B"],
        "profesor": "Profesor15"
    },
    "Educacion Fisica 1B": {
        "horas": 3,
        "disponibilidad": ["Dia5_Hora10_Curso1B","Dia1_Hora1_Curso1B", "Dia1_Hora2_Curso1B", "Dia1_Hora3_Curso1B", "Dia2_Hora1_Curso1B", "Dia2_Hora2_Curso1B", "Dia3_Hora1_Curso1B", "Dia3_Hora2_Curso1B"],
        "profesor": "Profesor16"
    }
}"""

"""materias = {
    "Matematica 1A": {
        "horas": 6,
        "disponibilidad": ["Dia1_Hora1_Curso1A", "Dia1_Hora2_Curso1A", "Dia3_Hora1_Curso1A", "Dia2_Hora1_Curso1A", "Dia5_Hora2_Curso1A", "Dia4_Hora1_Curso1A", "Dia1_Hora7_Curso1A", "Dia1_Hora8_Curso1A", "Dia3_Hora4_Curso1A"],
        "profesor": "Profesor1"
    
    },
    "Biologia 1B": {
        "horas": 3,
        "disponibilidad": ["Dia1_Hora3_Curso1B", "Dia2_Hora1_Curso1B", "Dia3_Hora2_Curso1B", "Dia1_Hora3_Curso1B", "Dia3_Hora2_Curso1B", "Dia4_Hora1_Curso1B"],
        "profesor": "Profesor1"
    },
    "Fisica 1A": {
        "horas": 5,
        "disponibilidad": ["Dia1_Hora1_Curso1A", "Dia2_Hora2_Curso1A", "Dia4_Hora1_Curso1A", "Dia3_Hora1_Curso1A", "Dia4_Hora2_Curso1A", "Dia5_Hora1_Curso1A"],
        "profesor": "Profesor2"
    },
    "Quimica 1B": {
        "horas": 4,
        "disponibilidad": ["Dia1_Hora1_Curso1B", "Dia2_Hora2_Curso1B", "Dia4_Hora1_Curso1B", "Dia2_Hora7_Curso1B", "Dia2_Hora6_Curso1B", "Dia4_Hora8_Curso1B"],
        "profesor": "Profesor3"
    },
}"""

materias = {
    "Matematica 1A": {
        "horas": 6,
        "disponibilidad": ["Dia1_Hora1_Curso1A", "Dia1_Hora2_Curso1A", "Dia3_Hora1_Curso1A", "Dia2_Hora1_Curso1A", "Dia5_Hora2_Curso1A", "Dia4_Hora1_Curso1A", "Dia1_Hora7_Curso1A", "Dia1_Hora8_Curso1A", "Dia3_Hora4_Curso1A"],
        "profesor": "Profesor1"
    
    },
    "Biologia 1B": {
        "horas": 3,
        "disponibilidad": ["Dia1_Hora1_Curso1B"],
        "profesor": "Profesor1"
    },
    "Fisica 1A": {
        "horas": 5,
        "disponibilidad": ["Dia1_Hora1_Curso1A", "Dia1_Hora2_Curso1A", "Dia3_Hora1_Curso1A", "Dia2_Hora1_Curso1A", "Dia5_Hora2_Curso1A", "Dia4_Hora1_Curso1A", "Dia1_Hora7_Curso1A", "Dia1_Hora8_Curso1A", "Dia3_Hora4_Curso1A"],
        "profesor": "Profesor2"
    },
    "Quimica 1B": {
        "horas": 4,
        "disponibilidad": ["Dia1_Hora3_Curso1B", "Dia2_Hora1_Curso1B", "Dia3_Hora2_Curso1B", "Dia1_Hora3_Curso1B", "Dia3_Hora2_Curso1B", "Dia4_Hora1_Curso1B"],
        "profesor": "Profesor3"
    },
}
""" caso de colapso total 1 sola hora
materias = {
    "Matematica 1A": {
        "horas": 6,
        "disponibilidad": ["Dia1_Hora1_Curso1A"],
        "profesor": "Profesor1"
    
    },
    "Biologia 1B": {
        "horas": 3,
        "disponibilidad": ["Dia1_Hora1_Curso1B"],
        "profesor": "Profesor1"
    },
    "Fisica 1A": {
        "horas": 5,
        "disponibilidad": ["Dia1_Hora1_Curso1A"],
        "profesor": "Profesor2"
    },
    "Quimica 1B": {
        "horas": 4,
        "disponibilidad": ["Dia1_Hora1_Curso1B"],
        "profesor": "Profesor3"
    },
}"""


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
for materia, horas_restantes in materias_sin_asignar.items():
    if horas_restantes > 0:
        print(f"Materia {materia} le quedaron {horas_restantes} horas sin asignar")
    else:
        print(f"Materia {materia} fue completamente asignada")

"""for materia in materias:
    for horario_curso in horarios_cursos:
        if pulp.value(asignacion[materia, horario_curso]) == 1:
            print(f"{materia} se enseñará en {horario_curso}")"""
            
# Crear horario
horario = {}
for curso in ["Curso1A", "Curso1B"]:
    for dia in range(1, 6):
        for hora in range(1, 11):
            horario[f"Dia{dia}_Hora{hora}_{curso}"] = None

# Llenar horario con las materias asignadas
for materia in materias:
    for horario_curso in horarios_cursos:
        if pulp.value(asignacion[materia, horario_curso]) == 1:
            horario[horario_curso] = materia

# Mostrar horario
for horario_curso, materia in horario.items():
    print(f"{horario_curso}: {materia}")
