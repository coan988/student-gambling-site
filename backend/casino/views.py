from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .utils import send_points_update
from .game_logic.blackjack import play_blackjack_round, dealer_play, determine_winner
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token



User = get_user_model()


# 🔹 Registrierung
@api_view(['POST'])
@csrf_exempt
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
@csrf_exempt
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


# Punkteverwaltung und Spiellogik blackjack
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def play_blackjack_view(request):
    bet = int(request.data.get("bet", 0))
    if bet <= 0:
        return Response({"error": "Ungültiger Einsatz"}, status=400)

    user = request.user
    from .game_logic.blackjack import play_blackjack_round
    game = play_blackjack_round()

    request.session["blackjack_state"] = {
        "deck": game["deck"],
        "player": game["player"],
        "dealer": game["dealer"],
        "bet": bet,
    }

    # Punkte abziehen
    user.points -= bet
    user.save()

    from .utils import send_points_update
    send_points_update(user.id, user.points)

    return Response({
        "player": game["player"],
        "dealer": game["dealer"]
    })






# Stand-Logik für Blackjack
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blackjack_stand(request):
    state = request.session.get("blackjack_state")
    if not state:
        return Response({"error": "Kein Spiel aktiv"}, status=400)

    deck = state["deck"]
    player = state["player"]
    dealer = state["dealer"]
    bet = state["bet"]

    dealer = dealer_play(deck, dealer)
    result = determine_winner(player, dealer)

    payout = 0
    if result == "win":
        payout = bet * 2
    elif result == "push":
        payout = bet

    user = User.objects.get(pk=request.user.pk)
    with transaction.atomic():
        user.points += payout
        user.save(update_fields=["points"])

    send_points_update(user.id, user.points)

    # Session zurücksetzen
    request.session.pop("blackjack_state", None)

    return Response({
        "result": result,
        "dealer": dealer,
        "player": player,
        "payout": payout,
        "new_points": user.points
    })


# Hit-Logik für Blackjack
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def blackjack_hit(request):
    state = request.session.get("blackjack_state")
    if not state:
        return Response({"error": "Kein aktives Spiel"}, status=400)

    deck = state["deck"]
    player = state["player"]
    dealer = state["dealer"]
    bet = state["bet"]

    from .game_logic.blackjack import draw_card, get_value
    player.append(draw_card(deck))
    player_value = get_value(player)

    # Bust (über 21)
    if player_value > 21:
        user = request.user
        # Einsatz ist schon bei Start abgezogen – keine doppelte Änderung
        user.save(update_fields=["points"])

        from .utils import send_points_update
        send_points_update(user.id, user.points)

        # Session löschen
        request.session.pop("blackjack_state", None)

        return Response({
            "player": player,
            "dealer": dealer,
            "result": "lose",
            "message": f"💥 Überkauft! Du verlierst {bet} Punkte.",
            "new_points": user.points
        })

    # Spiel geht weiter
    state["deck"] = deck
    state["player"] = player
    request.session["blackjack_state"] = state

    return Response({
        "player": player,
        "dealer": dealer,
        "result": "continue",
        "message": "Neue Karte gezogen."
    })


# 🔹 Leaderboard (Top 50 Spieler nach Punkten)
@api_view(['GET'])
def leaderboard_view(request):
    from django.db.models import F
    from django.contrib.auth import get_user_model
    User = get_user_model()

    query = request.query_params.get("search", None)

    if query:
        # Suche nach Username (case-insensitive)
        users = User.objects.filter(username__icontains=query).values("id", "username", "points")
        # Wenn in Top 50 enthalten, Rang berechnen
        top_users = list(User.objects.order_by("-points")[:50].values_list("id", flat=True))
        ranked = []
        for u in users:
            if u["id"] in top_users:
                rank = top_users.index(u["id"]) + 1
                u["rank"] = rank
            else:
                u["rank"] = None
            ranked.append(u)
        return Response(ranked)

    # Standard: Top 50 zurückgeben
    top_users = User.objects.order_by("-points")[:50]
    data = [
        {"rank": i + 1, "username": u.username, "points": u.points}
        for i, u in enumerate(top_users)
    ]
    return Response(data)

@api_view(['GET'])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Gibt den CSRF-Token explizit zurück, damit das Frontend ihn nutzen kann
    """
    return Response({
        'csrfToken': get_token(request)
    })
