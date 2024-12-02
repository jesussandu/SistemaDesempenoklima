from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Asegúrate de importar LogoutView
from .views import home_view, ver_kpis, completar_tarea, tareas_empleado, asignar_tareas_predefinidas, crear_tarea_predefinida, asignar_puntos_competencias
from . import views

urlpatterns = [
    # Ruta para login (Página de inicio de sesión)
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),

    # Ruta para logout (Cerrar sesión)
    path('logout/', LogoutView.as_view(), name='logout'),

    # Ruta para home (Página principal después del login)
    path('', home_view, name='home'),

    # Otras rutas
    path('ver_kpis/', ver_kpis, name='ver_kpis'),  # Ver KPIs
    path('completar_tarea/<int:tarea_id>/', completar_tarea, name='completar_tarea'),
    path('tareas_empleado/', tareas_empleado, name='tareas_empleado'),  # Ver tareas asignadas al empleado
    path('asignar_tareas/', asignar_tareas_predefinidas, name='asignar_tareas'),  # Asignar tareas predefinidas
    path('crear_tarea/', crear_tarea_predefinida, name='crear_tarea_predefinida'),  # Crear tarea predefinida
    path('asignar_puntos_competencias/<int:empleado_id>/', views.asignar_puntos_competencias, name='asignar_puntos_competencias'),
]
