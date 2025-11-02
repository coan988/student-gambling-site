from django.urls import path
from . import views

urlpatterns = [
    path('blackjack/', views.blackjack, name='blackjack'),
    path('roulette/', views.roulette, name='roulette'),
]
