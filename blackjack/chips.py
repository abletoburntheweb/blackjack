import random

suits = ['♥', '♦', '♣', '♠']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']

def card_value(rank, player_score):
    if rank in ["Валет", "Дама", "Король"]:
        return 10
    elif rank == "Туз":
        return 11 if player_score + 11 <= 21 else 1
    else:
        return int(rank)

def deal_card():
    suit = random.choice(suits)
    rank = random.choice(ranks)
    return suit, rank

def place_bet(player_balance):
    while True:
        try:
            bet_amount = int(input(f"У вас на счету {player_balance} фишек. Сколько хотите поставить? "))
            if bet_amount <= 0 or bet_amount > player_balance:
                print("Введите положительную сумму, которая не превышает ваш баланс.")
            else:
                return bet_amount
        except ValueError:
            print("Введите числовое значение.")