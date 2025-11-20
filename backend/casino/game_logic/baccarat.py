import random

# Kartenwerte für Baccarat
def card_value(card):
    """Return Baccarat card value."""
    rank = card % 13  # 0–12
    if rank >= 10:     # 10, J, Q, K → zählen als 0
        return 0
    return rank + 1    # Ass = 1, 2–9 bleiben normal

def draw_card(deck):
    """Eine Karte ziehen."""
    return deck.pop()

def baccarat_total(hand):
    """Total nach Baccarat-Regeln (Modulo 10)."""
    total = sum(card_value(c) for c in hand)
    return total % 10

def deal_initial_hands(deck):
    """Gibt zwei Starthände für Spieler und Banker."""
    player = [draw_card(deck), draw_card(deck)]
    banker = [draw_card(deck), draw_card(deck)]
    return player, banker

def should_player_draw(total):
    """Spieler zieht bei 0–5, steht bei 6–7, 8–9 = natural."""
    return total <= 5

def banker_draw_rule(banker_total, player_third_card):
    """
    Bank zieht anhand offizieller Baccarat-Regeln.
    player_third_card = None → Spieler hat keine gezogen.
    """
    if player_third_card is None:
        # Spieler stand → Banker zieht bei 0–5
        return banker_total <= 5

    # Third-card table rules
    ptc = card_value(player_third_card)

    if banker_total <= 2:
        return True
    elif banker_total == 3:
        return ptc != 8
    elif banker_total == 4:
        return 2 <= ptc <= 7
    elif banker_total == 5:
        return 4 <= ptc <= 7
    elif banker_total == 6:
        return ptc in [6, 7]
    else:
        return False

def play_baccarat_round():
    """
    Führt eine komplette Baccarat-Runde aus.
    Rückgabe:
      - player_hand
      - banker_hand
      - winner ("player", "banker", "tie")
    """

    # Standard 52-Karten Deck
    deck = list(range(52))
    random.shuffle(deck)

    player, banker = deal_initial_hands(deck)

    player_total = baccarat_total(player)
    banker_total = baccarat_total(banker)

    # Natural Win (8 oder 9)
    if player_total in [8, 9] or banker_total in [8, 9]:
        pass  # niemand zieht mehr
    else:
        # Spieler zieht?
        player_third_card = None
        if should_player_draw(player_total):
            player_third_card = draw_card(deck)
            player.append(player_third_card)
            player_total = baccarat_total(player)

        # Banker Regeln
        if banker_draw_rule(banker_total, player_third_card):
            banker.append(draw_card(deck))
            banker_total = baccarat_total(banker)

    # Gewinner bestimmen
    if player_total > banker_total:
        winner = "player"
    elif banker_total > player_total:
        winner = "banker"
    else:
        winner = "tie"

    return player, banker, winner