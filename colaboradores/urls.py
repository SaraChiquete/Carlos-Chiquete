from django.urls import path
from . import views

urlpatterns = [
    # LOGIN
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # PANEL DEL GERENTE
    path("gerente/", views.gerente_dashboard, name="gerente_dashboard"),
    path("gerente/colaboradores/", views.gerente_colaboradores, name="gerente_colaboradores"),
    path("gerente/horarios/", views.gerente_horarios, name="gerente_horarios"),
    path("gerente/horarios/pdf/", views.gerente_horarios_pdf, name="gerente_horarios_pdf"),
    path("gerente/<str:seccion>/", views.gerente_seccion_simple, name="gerente_seccion_simple"),
    path("gerente-perfil/", views.gerente_perfil, name="gerente_perfil"),

    # PORTAL DEL COLABORADOR
    path("colaborador/", views.colaborador_inicio, name="colaborador_inicio"),
    path("colaborador/horario/", views.colaborador_horario, name="colaborador_horario"),
    path("colaborador/perfil/", views.colaborador_perfil, name="colaborador_perfil"),
    path("colaborador/<str:seccion>/", views.colaborador_seccion_simple, name="colaborador_seccion_simple"),
]
