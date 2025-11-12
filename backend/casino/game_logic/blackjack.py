import random

SUITS = ["S", "H", "D", "C"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def create_deck():
    deck = [{"rank": r, "suit": s} for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck

def draw_card(deck):
    """Zieht die oberste Karte vom Deck und gibt sie zurück."""
    if not deck:
        raise ValueError("Das Kartendeck ist leer!")
    return deck.pop()

def get_value(hand):
    total = 0
    aces = 0
    for card in hand:
        if card["rank"] in ["J", "Q", "K"]:
            total += 10
        elif card["rank"] == "A":
            total += 11
            aces += 1
        else:
            total += int(card["rank"])
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def play_blackjack_round():
    """Startet eine neue Runde und gibt Karten für Spieler und Dealer zurück"""
    deck = create_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]  # zweite Karte verdeckt
    return {"player": player, "dealer": dealer, "deck": deck}

def dealer_play(deck, dealer_hand):
    """Dealer zieht bis mindestens 17"""
    while get_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
    return dealer_hand

def determine_winner(player, dealer):
    p_val = get_value(player)
    d_val = get_value(dealer)

    if p_val > 21:
        return "lose"
    elif d_val > 21:
        return "win"
    elif p_val > d_val:
        return "win"
    elif p_val < d_val:
        return "lose"
    else:
        return "push"