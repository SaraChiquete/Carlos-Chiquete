from . import data


def sesion_actual(request):
    """Hace disponible en TODOS los templates el rol y el nombre de la
    persona que inició sesión, para poder mostrarlo en el header/sidebar."""
    rol = request.session.get("rol")
    nombre = None

    if rol == "gerente":
        gerente = data.obtener_gerente(request.session.get("gerente_id"))
        nombre = gerente["nombre"] if gerente else None
    elif rol == "colaborador":
        colaborador = data.obtener_colaborador(request.session.get("colaborador_id"))
        nombre = colaborador["nombre"] if colaborador else None

    return {
        "sesion_rol": rol,
        "sesion_nombre": nombre,
    }
