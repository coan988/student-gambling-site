from django.shortcuts import render
from django.urls import reverse

# Startseite
def casino_starting_page(request):
    return render(request, 'casino_website.html')

def blackjack(request):
    return render(request, 'blackjack.html')

def roulette(request):
    return render(request, 'roulette.html')