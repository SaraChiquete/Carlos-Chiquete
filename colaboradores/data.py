"""
DATOS DE PRUEBA (MOCK DATA)
===========================

Este módulo reemplaza temporalmente a la base de datos.

Todas las estructuras son listas/diccionarios de Python que viven en
memoria mientras el servidor de Django está corriendo. Cuando el Gerente
"guarda" un horario, en realidad se está modificando la lista HORARIOS
de este archivo, y por eso el Portal del Colaborador puede leer el mismo
cambio inmediatamente (ambos leen de la misma fuente de datos).

IMPORTANTE PARA LA SIGUIENTE ETAPA (cuando se conecte una base de datos):
--------------------------------------------------------------------------
Cada función de este archivo (obtener_colaborador, obtener_horario_semanal,
guardar_horario_colaborador, etc.) está pensada para que, en el futuro,
su contenido se reemplace por consultas a los modelos de Django
(Colaborador.objects.get(...), Horario.objects.filter(...), etc.) SIN
tener que tocar las vistas (views.py) ni los templates. Las vistas nunca
acceden directamente a las listas de abajo: siempre pasan por estas
funciones. Esa es la "capa" que se deberá reemplazar.
"""

from datetime import datetime

# ---------------------------------------------------------------------------
# ÁREAS DISPONIBLES (fijas, según especificación del proyecto)
# ---------------------------------------------------------------------------
AREAS = [
    "Dulcería",
    "Taquilla",
    "Coffee",
    "Spiral",
    "Salas",
    "Limpieza profunda",
    "Proyección",
]

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


# ---------------------------------------------------------------------------
# COLABORADORES (datos ficticios, NO son empleados reales de Cinépolis)
# ---------------------------------------------------------------------------
COLABORADORES = [
    {"id": 1, "nombre": "Ana López", "puesto": "Colaborador", "area": "Dulcería",
     "telefono": "664-111-2201", "correo": "ana.lopez@cinepolis.mock", "fecha_ingreso": "2023-02-10"},
    {"id": 2, "nombre": "Carlos Pérez", "puesto": "Colaborador", "area": "Taquilla",
     "telefono": "664-111-2202", "correo": "carlos.perez@cinepolis.mock", "fecha_ingreso": "2022-11-05"},
    {"id": 3, "nombre": "María García", "puesto": "Colaborador", "area": "Coffee",
     "telefono": "664-111-2203", "correo": "maria.garcia@cinepolis.mock", "fecha_ingreso": "2023-06-19"},
    {"id": 4, "nombre": "Juan Rodríguez", "puesto": "Colaborador", "area": "Salas",
     "telefono": "664-111-2204", "correo": "juan.rodriguez@cinepolis.mock", "fecha_ingreso": "2021-09-01"},
    {"id": 5, "nombre": "Laura Hernández", "puesto": "Colaborador", "area": "Proyección",
     "telefono": "664-111-2205", "correo": "laura.hernandez@cinepolis.mock", "fecha_ingreso": "2023-01-15"},
    {"id": 6, "nombre": "Diego Martínez", "puesto": "Colaborador", "area": "Spiral",
     "telefono": "664-111-2206", "correo": "diego.martinez@cinepolis.mock", "fecha_ingreso": "2022-04-22"},
    {"id": 7, "nombre": "Fernanda Torres", "puesto": "Colaborador", "area": "Limpieza profunda",
     "telefono": "664-111-2207", "correo": "fernanda.torres@cinepolis.mock", "fecha_ingreso": "2023-08-30"},
    {"id": 8, "nombre": "Ricardo Sánchez", "puesto": "Colaborador", "area": "Dulcería",
     "telefono": "664-111-2208", "correo": "ricardo.sanchez@cinepolis.mock", "fecha_ingreso": "2022-07-12"},
    {"id": 9, "nombre": "Paola Jiménez", "puesto": "Colaborador", "area": "Taquilla",
     "telefono": "664-111-2209", "correo": "paola.jimenez@cinepolis.mock", "fecha_ingreso": "2023-03-03"},
    {"id": 10, "nombre": "Héctor Ramírez", "puesto": "Colaborador", "area": "Coffee",
     "telefono": "664-111-2210", "correo": "hector.ramirez@cinepolis.mock", "fecha_ingreso": "2021-12-20"},
]

# GERENTE(S) de prueba (no están en COLABORADORES porque su rol es distinto)
GERENTES = [
    {"id": 100, "nombre": "Roberto Sánchez", "puesto": "Gerente de Unidad"},
]


# ---------------------------------------------------------------------------
# USUARIOS DE PRUEBA PARA EL LOGIN
# usuario / password muy simples porque "no es necesario implementar
# todavía un sistema de autenticación avanzado" (se reemplazará después
# por el sistema de autenticación de Django: django.contrib.auth).
# ---------------------------------------------------------------------------
USUARIOS = [
    {"usuario": "gerente", "password": "1234", "rol": "gerente", "gerente_id": 100},
    {"usuario": "ana", "password": "1234", "rol": "colaborador", "colaborador_id": 1},
    {"usuario": "carlos", "password": "1234", "rol": "colaborador", "colaborador_id": 2},
    {"usuario": "maria", "password": "1234", "rol": "colaborador", "colaborador_id": 3},
    {"usuario": "juan", "password": "1234", "rol": "colaborador", "colaborador_id": 4},
    {"usuario": "laura", "password": "1234", "rol": "colaborador", "colaborador_id": 5},
]


# ---------------------------------------------------------------------------
# HORARIOS
# Estructura: { colaborador_id: { "Lunes": {"area": ..., "entrada": ..., "salida": ...}, ... } }
# "Descanso" se representa con area=None
# ---------------------------------------------------------------------------
HORARIOS = {
    1: {  # Ana López -> ejemplo exacto de la especificación
        "Lunes": {"area": "Dulcería", "entrada": "12:00", "salida": "20:00"},
        "Martes": {"area": "Dulcería", "entrada": "12:00", "salida": "20:00"},
        "Miércoles": {"area": None, "entrada": None, "salida": None},
        "Jueves": {"area": "Taquilla", "entrada": "14:00", "salida": "22:00"},
        "Viernes": {"area": "Dulcería", "entrada": "12:00", "salida": "20:00"},
        "Sábado": {"area": None, "entrada": None, "salida": None},
        "Domingo": {"area": None, "entrada": None, "salida": None},
    },
    2: {  # Carlos Pérez
        "Lunes": {"area": "Taquilla", "entrada": "14:00", "salida": "22:00"},
        "Martes": {"area": None, "entrada": None, "salida": None},
        "Miércoles": {"area": "Taquilla", "entrada": "14:00", "salida": "22:00"},
        "Jueves": {"area": "Taquilla", "entrada": "14:00", "salida": "22:00"},
        "Viernes": {"area": "Taquilla", "entrada": "14:00", "salida": "22:00"},
        "Sábado": {"area": "Taquilla", "entrada": "12:00", "salida": "20:00"},
        "Domingo": {"area": None, "entrada": None, "salida": None},
    },
}


def _horario_vacio():
    return {dia: {"area": None, "entrada": None, "salida": None} for dia in DIAS_SEMANA}


# Nos asegura que TODOS los colaboradores tengan una entrada en HORARIOS
for _c in COLABORADORES:
    HORARIOS.setdefault(_c["id"], _horario_vacio())


# ---------------------------------------------------------------------------
# ASISTENCIAS / FALTAS / INCIDENCIAS / AMONESTACIONES (resumen ficticio)
# ---------------------------------------------------------------------------
ASISTENCIAS = {
    1: [{"fecha": "2026-09-01", "estatus": "A tiempo"},
        {"fecha": "2026-09-02", "estatus": "A tiempo"},
        {"fecha": "2026-09-04", "estatus": "Retardo"}],
    2: [{"fecha": "2026-09-01", "estatus": "A tiempo"},
        {"fecha": "2026-09-03", "estatus": "A tiempo"}],
}

FALTAS = {
    1: [{"fecha": "2026-08-15", "motivo": "Cita médica"}],
    2: [],
}

INCIDENCIAS = {
    1: [{"fecha": "2026-08-20", "descripcion": "Llegó 10 minutos tarde por tráfico"}],
    2: [{"fecha": "2026-07-30", "descripcion": "Cambio de turno acordado con el gerente"}],
}

AMONESTACIONES = {
    1: [],
    2: [{"fecha": "2026-06-10", "motivo": "Uniforme incompleto", "nivel": "Verbal"}],
}

for _c in COLABORADORES:
    ASISTENCIAS.setdefault(_c["id"], [])
    FALTAS.setdefault(_c["id"], [])
    INCIDENCIAS.setdefault(_c["id"], [])
    AMONESTACIONES.setdefault(_c["id"], [])


# ---------------------------------------------------------------------------
# FUNCIONES DE ACCESO A DATOS
# (esta es la capa que en el futuro se reemplaza por el ORM de Django)
# ---------------------------------------------------------------------------

def obtener_todos_colaboradores():
    return COLABORADORES


def obtener_colaborador(colaborador_id):
    for c in COLABORADORES:
        if c["id"] == colaborador_id:
            return c
    return None


def obtener_colaboradores_por_area(area):
    return [c for c in COLABORADORES if c["area"] == area]


def obtener_horario_semanal(colaborador_id):
    """Regresa una lista ordenada [ {dia, area, entrada, salida}, ... ]"""
    horario = HORARIOS.get(colaborador_id, _horario_vacio())
    return [
        {
            "dia": dia,
            "area": horario[dia]["area"],
            "entrada": horario[dia]["entrada"],
            "salida": horario[dia]["salida"],
        }
        for dia in DIAS_SEMANA
    ]


def obtener_proximo_turno(colaborador_id):
    """Busca, a partir de hoy, el próximo día (dentro de los 7 días de la
    semana) que tenga un turno asignado (area distinto de None)."""
    hoy_idx = datetime.now().weekday()  # 0 = Lunes ... 6 = Domingo
    horario = HORARIOS.get(colaborador_id, _horario_vacio())
    for offset in range(7):
        idx = (hoy_idx + offset) % 7
        dia = DIAS_SEMANA[idx]
        turno = horario[dia]
        if turno["area"]:
            return {"dia": dia, **turno}
    return None


def guardar_horario_colaboradores(colaborador_ids, dia, area, entrada, salida):
    """Asigna el mismo día/área/horario a una lista de colaboradores.
    Si entrada/salida vienen vacíos, se guarda como 'Descanso'."""
    for cid in colaborador_ids:
        HORARIOS.setdefault(cid, _horario_vacio())
        if not entrada or not salida:
            HORARIOS[cid][dia] = {"area": None, "entrada": None, "salida": None}
        else:
            HORARIOS[cid][dia] = {"area": area, "entrada": entrada, "salida": salida}


def obtener_resumen_dashboard():
    total = len(COLABORADORES)
    return {
        "total_colaboradores": total,
        "colaboradores_activos": total,  # dato ficticio, todos activos por ahora
        "total_asistencias": sum(len(v) for v in ASISTENCIAS.values()),
        "total_faltas": sum(len(v) for v in FALTAS.values()),
        "total_incidencias": sum(len(v) for v in INCIDENCIAS.values()),
        "total_amonestaciones": sum(len(v) for v in AMONESTACIONES.values()),
        "areas": AREAS,
    }


def obtener_usuario(usuario, password):
    for u in USUARIOS:
        if u["usuario"] == usuario and u["password"] == password:
            return u
    return None


def obtener_gerente(gerente_id):
    for g in GERENTES:
        if g["id"] == gerente_id:
            return g
    return None
