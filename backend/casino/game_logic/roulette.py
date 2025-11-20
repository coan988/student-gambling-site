import random

ROULETTE_COLORS = {
    0: "green",
    1:"red", 2:"black", 3:"red", 4:"black", 5:"red", 6:"black",
    7:"red", 8:"black", 9:"red", 10:"black", 11:"black", 12:"red",
    13:"black", 14:"red", 15:"black", 16:"red", 17:"black", 18:"red",
    19:"red", 20:"black", 21:"red", 22:"black", 23:"red", 24:"black",
    25:"red", 26:"black", 27:"red", 28:"black", 29:"black", 30:"red",
    31:"black", 32:"red", 33:"black", 34:"red", 35:"black", 36:"red",
}

def play_roulette(bet_type, amount, number=None):

    result_number = random.randint(0, 36)
    result_color = ROULETTE_COLORS[result_number]
    win_amount = 0

    # Wette auf Zahl
    if bet_type == "number":
        if number is not None and int(number) == result_number:
            win_amount = amount * 35

    # Wette auf Farbe
    elif bet_type == "color":
        if result_color != "green" and number == result_color:
            win_amount = amount * 2

    # Wette auf Gerade/Ungerade
    elif bet_type == "even_odd":
        if result_number != 0:
            if (result_number % 2 == 0 and number == "even") or \
               (result_number % 2 == 1 and number == "odd"):
                win_amount = amount * 2

    return result_number, result_color, win_amount
