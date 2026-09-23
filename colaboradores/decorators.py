"""
Decoradores de control de acceso.

Como todavía no usamos django.contrib.auth, el "login" se simula
guardando el rol y el id del usuario en la sesión (request.session).
Estos decoradores revisan esa sesión antes de dejar pasar a cada vista.

Cuando se conecte el sistema de autenticación real de Django, estos
decoradores se pueden sustituir por @login_required y @user_passes_test
sin cambiar la forma en que las vistas están escritas.
"""

from functools import wraps
from django.shortcuts import redirect


def gerente_requerido(vista):
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if request.session.get("rol") != "gerente":
            return redirect("login")
        return vista(request, *args, **kwargs)
    return wrapper


def colaborador_requerido(vista):
    @wraps(vista)
    def wrapper(request, *args, **kwargs):
        if request.session.get("rol") != "colaborador":
            return redirect("login")
        return vista(request, *args, **kwargs)
    return wrapper
