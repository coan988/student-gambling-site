from django.urls import path
from . import views

urlpatterns = [
    # Registrierung und Login als API-Endpunkte
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('session/', views.session_view, name='check_session'),
    path('logout/', views.logout_user, name='logout_user'),
]
