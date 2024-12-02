from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    role = models.CharField(max_length=10, choices=ROLES, default='empleado')


    # Resolver conflictos añadiendo `related_name` único
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_groups',  # Nombre único para evitar conflictos
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Nombre único para evitar conflictos
        blank=True,
    )

class TareaPredefinida(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    periodicidad = models.CharField(max_length=20, choices=[('diario', 'Diario'), ('semanal', 'Semanal'), ('mensual', 'Mensual')])

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tarea_predefinida = models.ForeignKey(TareaPredefinida, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default='pendiente')  

    def __str__(self):
        return self.nombre

# KPI asociado a cada empleado
class KPI(models.Model):
    empleado = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    tareas_completadas = models.IntegerField(default=0)
    tareas_totales = models.IntegerField(default=0)
    
    # Puntos por competencias
    trabajo_en_equipo = models.IntegerField(default=0)  # Puntos de trabajo en equipo
    adaptacion = models.IntegerField(default=0)         # Puntos de adaptación
    comunicacion = models.IntegerField(default=0)       # Puntos de comunicación
    resolucion_problemas = models.IntegerField(default=0)  # Puntos de resolución de problemas
    
    @property
    def tasa_finalizacion(self):
        if self.tareas_totales == 0:
            return 0
        return (self.tareas_completadas / self.tareas_totales) * 100

    @property
    def puntos_competencias(self):
        # Sumar los puntos de las competencias
        return self.trabajo_en_equipo + self.adaptacion + self.comunicacion + self.resolucion_problemas

    @property
    def puntuacion_total(self):
        # Puedes decidir cómo calcular el KPI total. Aquí simplemente sumamos las tareas completadas y los puntos de competencias
        return self.tasa_finalizacion + self.puntos_competencias
