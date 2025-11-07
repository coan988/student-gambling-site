from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

User = get_user_model()


# 🔹 Registrierung
@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Alle Felder (username, email, password) sind erforderlich.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Benutzername existiert bereits.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'E-Mail wird bereits verwendet.'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Benutzer erstellen
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        points=1000  # Startpunkte
    )

    # Benutzer automatisch einloggen
    login(request, user)

    return Response({
        'message': 'Benutzer erfolgreich registriert.',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'points': user.points
        }
    }, status=status.HTTP_201_CREATED)


# 🔹 Login
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Benutzername und Passwort sind erforderlich.'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login erfolgreich.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'points': user.points
            }
        })
    else:
        return Response({'error': 'Ungültige Zugangsdaten.'},
                        status=status.HTTP_401_UNAUTHORIZED)


# 🔹 Logout
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logout erfolgreich.'})


# 🔹 Sessionprüfung (wird vom Frontend aufgerufen)
@ensure_csrf_cookie  # sorgt dafür, dass csrftoken-Cookie gesetzt wird
@api_view(['GET'])
def session_view(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({
            'authenticated': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'points': user.points
            }
        })
    else:
        return Response({'authenticated': False})