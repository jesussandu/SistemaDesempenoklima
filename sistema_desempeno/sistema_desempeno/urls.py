from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin de Django
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),  # Ruta para el login
    path('logout/', LogoutView.as_view(), name='logout'),  # Ruta para el logout
    path('', LoginView.as_view(template_name='core/login.html'), name='login'),  # Ruta raíz redirige al login
    path('home/', home_view, name='home'),  # Redirige a home después de login
    path('core/', include('core.urls')),  # Incluye las rutas de la app 'core'
]
