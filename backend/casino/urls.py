from django.urls import path
from . import views

urlpatterns = [
    # Registrierung und Login als API-Endpunkte
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('session/', views.session_view, name='check_session'),
    path('logout/', views.logout_user, name='logout_user'),
    path('play-blackjack/', views.play_blackjack_view, name='play_blackjack'),
    path('blackjack-stand/', views.blackjack_stand, name='blackjack_stand'),
    path('blackjack-hit/', views.blackjack_hit, name='blackjack_hit'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard_view'),
]
