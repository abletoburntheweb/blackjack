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


def game():
    print("Добро пожаловать!")

    player_balance = 100
    while player_balance > 0:
        bet = place_bet(player_balance)
        player_balance -= bet

        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]

        player_score = sum([card_value(card[1], 0) for card in player_hand])
        dealer_score = sum([card_value(card[1], 0) for card in dealer_hand])

        print("Ваши карты:", player_hand[0][1], player_hand[0][0], "и", player_hand[1][1], player_hand[1][0])
        print("Сумма ваших карт:", player_score)
        print("Карта дилера:", dealer_hand[0][1], dealer_hand[0][0])

        while True:
            choice = input("Хотите взять еще карту? (Да/Нет): ").lower()
            if choice == "да":
                new_card = deal_card()
                player_hand.append(new_card)
                player_score += card_value(new_card[1], player_score)
                print("Вы получили карту:", new_card[1], new_card[0])
                print("Сумма ваших карт:", player_score)

                if player_score > 21:
                    print("Перебор! У вас больше 21. Вы проиграли.")
                    break
            else:
                break

        while dealer_score < 17:
            new_card = deal_card()
            dealer_hand.append(new_card)
            dealer_score += card_value(new_card[1], dealer_score)
            print("Дилер получил карту:", new_card[1], new_card[0])

        if dealer_score > 21 or player_score > dealer_score:
            print("Вы выиграли! Получаете двойную ставку.")
            player_balance += bet * 2
        elif dealer_score > player_score:
            print("Дилер выиграл. Вы проиграли.")
        else:
            print("Ничья! Вам возвращается ставка.")

        print("У вас на счету:", player_balance, "фишек")

    print("У вас закончились фишки. Game over!")


game()
