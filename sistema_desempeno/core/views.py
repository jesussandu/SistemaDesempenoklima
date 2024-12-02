from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, TareaPredefinidaForm
from .models import TareaPredefinida, Tarea, Usuario, KPI
from .forms import KPIPointsForm

# Función para verificar si el usuario es administrador
def admin_check(user):
    return user.role == 'admin'  # Verifica si el usuario tiene el rol 'admin'

@login_required
def home_view(request):
    if request.user.role == 'admin':  # Verificamos si el usuario es administrador
        return render(request, 'core/home_admin.html')  # Página de inicio para administradores
    else:
        return render(request, 'core/home_employee.html')  # Página de inicio para empleados

# Vista para el login personalizado
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')  # Redirige al home después de iniciar sesión

# Vista para crear una tarea predefinida
def crear_tarea_predefinida(request):
    if request.method == 'POST':
        form = TareaPredefinidaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la tarea predefinida
            return redirect('ver_tareas')  # Redirige a la lista de tareas predefinidas
    else:
        form = TareaPredefinidaForm()
    
    return render(request, 'core/crear_tarea_predefinida.html', {'form': form})

# Vista para asignar tareas predefinidas a empleados (solo para administradores)
@login_required
@user_passes_test(admin_check)
def asignar_tareas_predefinidas(request):
    empleados = Usuario.objects.filter(role='empleado')  # Filtramos solo los empleados
    tareas_predefinidas = TareaPredefinida.objects.all()  # Traemos todas las tareas predefinidas

    if request.method == 'POST':
        # Asignar las tareas seleccionadas a los empleados
        for empleado in empleados:
            for tarea in tareas_predefinidas:
                tarea_asignada = request.POST.get(f"tarea_{tarea.id}_{empleado.id}")
                if tarea_asignada:  # Si la tarea ha sido seleccionada
                    Tarea.objects.create(tarea_predefinida=tarea, usuario=empleado)
        return redirect('ver_kpis')  # Redirigimos a la vista de KPIs después de asignar las tareas

    return render(request, 'core/asignar_tarea.html', {
        'empleados': empleados,
        'tareas_predefinidas': tareas_predefinidas
    })

# Vista para ver los KPIs de los empleados
@login_required
def ver_kpis(request):
    if request.user.role == 'admin':  
        kpis = KPI.objects.all()  # El administrador ve todos los KPIs
    elif request.user.role == 'empleado':  # Si el usuario es empleado
        kpis = KPI.objects.filter(empleado=request.user)  # El empleado solo ve su propio KPI
    else:
        kpis = []  

    return render(request, 'core/ver_kpis.html', {'kpis': kpis})

# Vista para completar una tarea
@login_required
def completar_tarea(request, tarea_id):
    # Obtén la tarea a partir del ID
    tarea = Tarea.objects.get(id=tarea_id)
    
    # Cambiar el estado de la tarea a 'completada' y actualizar la fecha
    tarea.estado = 'completada'
    tarea.fecha_completada = timezone.now()
    tarea.save()

    # Actualizar o crear el KPI del empleado correspondiente
    kpi, created = KPI.objects.get_or_create(empleado=request.user)
    kpi.tareas_completadas += 1  # Incrementar el número de tareas completadas
    kpi.save()

    # Redirigir al usuario a la página de tareas del empleado
    return redirect('tareas_empleado')

# Vista para ver las tareas asignadas al empleado
@login_required
def tareas_empleado(request):
    tareas = Tarea.objects.filter(usuario=request.user)  # Filtra las tareas del usuario actual
    return render(request, 'core/tareas_empleado.html', {'tareas': tareas})

# Vista para agregar una tarea predefinida
def agregar_tarea(request):
    if request.method == 'POST':
        form = TareaPredefinidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_tareas')  # Redirige a una vista que muestra las tareas
    else:
        form = TareaPredefinidaForm()
    return render(request, 'core/agregar_tarea.html', {'form': form})

# Vista para ver las tareas predefinidas
def ver_tareas(request):
    tareas = TareaPredefinida.objects.all()
    return render(request, 'core/ver_tareas.html', {'tareas': tareas})

def admin_check(user):
    return user.is_staff  

@login_required
@user_passes_test(admin_check)  # Solo los administradores pueden acceder a esta vista
def asignar_puntos_competencias(request, empleado_id):
    # Asegúrate de que el empleado existe
    try:
        empleado = Usuario.objects.get(id=empleado_id)
    except Usuario.DoesNotExist:
        return redirect('ver_kpis')  # Si el empleado no existe, redirige a la vista de KPIs

    # Si el método es POST, actualizamos los puntos de competencias
    if request.method == 'POST':
        # Obtener o crear el KPI para el empleado
        kpi, created = KPI.objects.get_or_create(empleado=empleado)
        
        # Obtener los puntos desde el POST y asegurarse de que sean enteros
        kpi.trabajo_en_equipo = int(request.POST.get('trabajo_en_equipo', 0))
        kpi.adaptacion = int(request.POST.get('adaptacion', 0))
        kpi.comunicacion = int(request.POST.get('comunicacion', 0))
        kpi.resolucion_problemas = int(request.POST.get('resolucion_problemas', 0))
        
        kpi.save()  # Guardamos el KPI con los nuevos valores de los puntos

        return redirect('ver_kpis')  # Redirigimos a la vista de KPIs después de guardar

    # Si no es un POST, simplemente mostramos el formulario
    return render(request, 'core/asignar_puntos_competencias.html', {'empleado': empleado})