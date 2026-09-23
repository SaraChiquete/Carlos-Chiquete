from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from . import data
from .decorators import gerente_requerido, colaborador_requerido


# ===========================================================================
# LOGIN / LOGOUT
# ===========================================================================

def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get("usuario", "").strip()
        password = request.POST.get("password", "").strip()
        user = data.obtener_usuario(usuario, password)

        if user is None:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, "login.html")

        request.session["rol"] = user["rol"]
        if user["rol"] == "gerente":
            request.session["gerente_id"] = user["gerente_id"]
            return redirect("gerente_dashboard")
        else:
            request.session["colaborador_id"] = user["colaborador_id"]
            return redirect("colaborador_inicio")

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


# ===========================================================================
# PANEL DEL GERENTE
# ===========================================================================

@gerente_requerido
def gerente_dashboard(request):
    resumen = data.obtener_resumen_dashboard()
    return render(request, "gerente/dashboard.html", {"resumen": resumen})


@gerente_requerido
def gerente_colaboradores(request):
    area_filtro = request.GET.get("area", "")
    busqueda = request.GET.get("q", "").strip().lower()

    colaboradores = data.obtener_todos_colaboradores()
    if area_filtro:
        colaboradores = [c for c in colaboradores if c["area"] == area_filtro]
    if busqueda:
        colaboradores = [c for c in colaboradores if busqueda in c["nombre"].lower()]

    contexto = {
        "colaboradores": colaboradores,
        "areas": data.AREAS,
        "area_filtro": area_filtro,
        "busqueda": busqueda,
    }
    return render(request, "gerente/colaboradores.html", contexto)


@gerente_requerido
def gerente_horarios(request):
    """
    Módulo principal de asignación de horarios.

    Flujo:
      1. GET  ?area=Dulcería            -> muestra colaboradores de esa área
      2. POST (guardar_horario)         -> guarda día/entrada/salida para
                                            los colaboradores seleccionados
    """
    area_seleccionada = request.GET.get("area", "") or request.POST.get("area", "")
    colaboradores_area = []
    if area_seleccionada:
        colaboradores_area = data.obtener_colaboradores_por_area(area_seleccionada)

    if request.method == "POST" and request.POST.get("accion") == "guardar_horario":
        colaborador_ids = [int(cid) for cid in request.POST.getlist("colaboradores")]
        dia = request.POST.get("dia")
        entrada = request.POST.get("entrada")
        salida = request.POST.get("salida")
        es_descanso = request.POST.get("es_descanso") == "on"

        if not colaborador_ids:
            messages.error(request, "Selecciona al menos un colaborador.")
        elif not dia:
            messages.error(request, "Selecciona un día.")
        else:
            data.guardar_horario_colaboradores(
                colaborador_ids=colaborador_ids,
                dia=dia,
                area=area_seleccionada,
                entrada=None if es_descanso else entrada,
                salida=None if es_descanso else salida,
            )
            nombres = ", ".join(
                c["nombre"] for c in colaboradores_area if c["id"] in colaborador_ids
            )
            messages.success(
                request,
                f"Horario del {dia} guardado para: {nombres}."
            )

    # Tabla de horario semanal de todos los colaboradores del área (para revisar)
    horarios_area = []
    for c in colaboradores_area:
        horarios_area.append({
            "colaborador": c,
            "semana": data.obtener_horario_semanal(c["id"]),
        })

    contexto = {
        "areas": data.AREAS,
        "dias": data.DIAS_SEMANA,
        "area_seleccionada": area_seleccionada,
        "colaboradores_area": colaboradores_area,
        "horarios_area": horarios_area,
    }
    return render(request, "gerente/horarios.html", contexto)


@gerente_requerido
def gerente_horarios_pdf(request):
    """Genera el PDF general o el de un área específica."""
    from .pdf_utils import generar_pdf_horarios

    area = request.GET.get("area", "")
    colaboradores = (
        data.obtener_colaboradores_por_area(area) if area else data.obtener_todos_colaboradores()
    )

    filas = []
    for c in colaboradores:
        semana = {h["dia"]: h for h in data.obtener_horario_semanal(c["id"])}
        filas.append((c, semana))

    pdf_bytes = generar_pdf_horarios(area=area or "Todas las áreas", filas=filas, dias=data.DIAS_SEMANA)

    nombre_archivo = f"horario_{area or 'general'}.pdf".replace(" ", "_")
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
    return response


@gerente_requerido
def gerente_seccion_simple(request, seccion):
    """
    Páginas del menú lateral que por ahora solo muestran un listado
    ficticio general (Asistencias, Faltas, Incidencias, Amonestaciones),
    ya que la prioridad de esta primera versión es el módulo de horarios.
    """
    fuentes = {
        "asistencias": (data.ASISTENCIAS, "Asistencias"),
        "faltas": (data.FALTAS, "Faltas"),
        "incidencias": (data.INCIDENCIAS, "Incidencias"),
        "amonestaciones": (data.AMONESTACIONES, "Amonestaciones"),
    }
    fuente, titulo = fuentes[seccion]

    filas = []
    for c in data.obtener_todos_colaboradores():
        for registro in fuente.get(c["id"], []):
            filas.append({"colaborador": c, **registro})

    return render(request, "gerente/seccion_simple.html", {
        "titulo": titulo,
        "seccion": seccion,
        "filas": filas,
    })


@gerente_requerido
def gerente_perfil(request):
    gerente = data.obtener_gerente(request.session.get("gerente_id"))
    return render(request, "gerente/perfil.html", {"gerente": gerente})


# ===========================================================================
# PORTAL DEL COLABORADOR
# ===========================================================================

def _colaborador_actual(request):
    return data.obtener_colaborador(request.session.get("colaborador_id"))


@colaborador_requerido
def colaborador_inicio(request):
    colaborador = _colaborador_actual(request)
    proximo_turno = data.obtener_proximo_turno(colaborador["id"])
    contexto = {
        "colaborador": colaborador,
        "primer_nombre": colaborador["nombre"].split(" ")[0],
        "proximo_turno": proximo_turno,
        "num_asistencias": len(data.ASISTENCIAS.get(colaborador["id"], [])),
        "num_faltas": len(data.FALTAS.get(colaborador["id"], [])),
        "num_incidencias": len(data.INCIDENCIAS.get(colaborador["id"], [])),
        "num_amonestaciones": len(data.AMONESTACIONES.get(colaborador["id"], [])),
    }
    return render(request, "colaborador/inicio.html", contexto)


@colaborador_requerido
def colaborador_horario(request):
    colaborador = _colaborador_actual(request)
    semana = data.obtener_horario_semanal(colaborador["id"])
    proximo_turno = data.obtener_proximo_turno(colaborador["id"])
    return render(request, "colaborador/horario.html", {
        "colaborador": colaborador,
        "semana": semana,
        "proximo_turno": proximo_turno,
    })


@colaborador_requerido
def colaborador_seccion_simple(request, seccion):
    colaborador = _colaborador_actual(request)
    fuentes = {
        "asistencias": (data.ASISTENCIAS, "Mis asistencias"),
        "faltas": (data.FALTAS, "Mis faltas"),
        "incidencias": (data.INCIDENCIAS, "Mis incidencias"),
        "amonestaciones": (data.AMONESTACIONES, "Mis amonestaciones"),
    }
    fuente, titulo = fuentes[seccion]
    registros = fuente.get(colaborador["id"], [])

    return render(request, "colaborador/seccion_simple.html", {
        "colaborador": colaborador,
        "titulo": titulo,
        "seccion": seccion,
        "registros": registros,
    })


@colaborador_requerido
def colaborador_perfil(request):
    colaborador = _colaborador_actual(request)
    return render(request, "colaborador/perfil.html", {"colaborador": colaborador})
