from django.shortcuts import render

# Create your views here.
def casino(request):
    return render(request, 'casino_website.html')