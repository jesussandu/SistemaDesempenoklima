from django import forms
from .models import TareaPredefinida
from django.contrib.auth.forms import AuthenticationForm
from .models import KPI

# Formulario para crear tareas predefinidas
class TareaPredefinidaForm(forms.ModelForm):
    class Meta:
        model = TareaPredefinida
        fields = ['nombre', 'descripcion', 'periodicidad']  # Asegúrate de que estos campos estén en tu modelo

# Formulario para la autenticación de usuarios (inicio de sesión)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

class KPIPointsForm(forms.ModelForm):
    class Meta:
        model = KPI
        fields = ['trabajo_en_equipo', 'adaptacion', 'comunicacion', 'resolucion_problemas']

    trabajo_en_equipo = forms.IntegerField(label='Trabajo en equipo', min_value=0, max_value=100)
    adaptacion = forms.IntegerField(label='Adaptación', min_value=0, max_value=100)
    comunicacion = forms.IntegerField(label='Comunicación', min_value=0, max_value=100)
    resolucion_problemas = forms.IntegerField(label='Resolución de problemas', min_value=0, max_value=100)
