from django.contrib import admin
from .models import Tarea, TareaPredefinida, Usuario
from django.contrib.auth.admin import UserAdmin

class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'fecha_creacion', 'tarea_predefinida', 'usuario')

# Personalización para el modelo TareaPredefinida
class TareaPredefinidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'periodicidad')
    search_fields = ('nombre', 'descripcion')

# Personalización para el modelo Usuario
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')  # Añadimos el campo 'role'
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Añadimos el campo 'role' en el formulario de edición
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Añadimos el campo 'role' en el formulario de creación
    )

# Registro de los modelos con las clases personalizadas
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Tarea, TareaAdmin)
admin.site.register(TareaPredefinida, TareaPredefinidaAdmin)
