"""
MODELOS DE DJANGO (siguiente etapa del proyecto)
=================================================

En esta primera versión el sistema NO usa base de datos: toda la
información vive como datos de prueba en `data.py`.

Cuando llegue el momento de conectar una base de datos real, los
modelos que reemplazarán a esas listas son, aproximadamente:

    class Colaborador(models.Model):
        nombre = models.CharField(max_length=150)
        puesto = models.CharField(max_length=100)
        area = models.CharField(max_length=50, choices=AREA_CHOICES)
        telefono = models.CharField(max_length=20, blank=True)
        correo = models.EmailField(blank=True)
        fecha_ingreso = models.DateField()
        usuario = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    class Horario(models.Model):
        colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name="horarios")
        dia = models.CharField(max_length=15, choices=DIA_CHOICES)
        area = models.CharField(max_length=50, choices=AREA_CHOICES, null=True, blank=True)
        entrada = models.TimeField(null=True, blank=True)
        salida = models.TimeField(null=True, blank=True)

    class Asistencia(models.Model):
        colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
        fecha = models.DateField()
        estatus = models.CharField(max_length=30)

    class Falta(models.Model):
        colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
        fecha = models.DateField()
        motivo = models.CharField(max_length=255)

    class Incidencia(models.Model):
        colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
        fecha = models.DateField()
        descripcion = models.TextField()

    class Amonestacion(models.Model):
        colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
        fecha = models.DateField()
        motivo = models.CharField(max_length=255)
        nivel = models.CharField(max_length=30)

Para activarlos:
  1. Descomentar/crear estas clases aquí.
  2. Agregar 'django.contrib.admin', 'django.contrib.auth' y
     'django.contrib.contenttypes' de nuevo a INSTALLED_APPS en settings.py.
  3. Ejecutar: python manage.py makemigrations && python manage.py migrate
  4. Reemplazar, dentro de data.py, el cuerpo de cada función
     (obtener_colaborador, obtener_horario_semanal, guardar_horario_colaboradores...)
     por su equivalente en el ORM de Django. Las vistas (views.py) y los
     templates NO tienen que cambiar porque siempre llaman a esas funciones.
"""
