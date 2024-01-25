#переписать функцию туза
import random

suits = ['♥', '♦', '♣', '♠']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']


def card_value(rank):
    if rank in ["Валет", "Дама", "Король"]:
        return 10
    elif rank == "Туз":
        return 11
    else:
        return int(rank)


def deal_card():
    suit = random.choice(suits)
    rank = random.choice(ranks)
    return suit, rank

'''def hand_sum(hand):
тут должна быть функция, проверяющая,
если игроку выпал Туз, и сумма очков с ним 
больше 21, то нужно вычесть 10 очков
'''

def game():
    print("Добро пожаловать!")

    # Карты игрока
    player_card1_suit, player_card1_rank = deal_card()
    player_card2_suit, player_card2_rank = deal_card()
    player_score = card_value(player_card1_rank) + card_value(player_card2_rank)

    # Карты дилера
    dealer_card1_suit, dealer_card1_rank = deal_card()
    dealer_card2_suit, dealer_card2_rank = deal_card()
    dealer_score = card_value(dealer_card1_rank) + card_value(dealer_card2_rank)

    print("Ваши карты:", player_card1_rank, player_card1_suit, "и", player_card2_rank, player_card2_suit)
    print("Сумма ваших карт:", player_score)
    print("Карта дилера:", dealer_card1_rank, dealer_card1_suit)

    if player_score == 21:
        print("У вас блэкджек! goddamn")
        return

    while True:
        player_choice = input("Хотите взять ещё карту? (Да/Нет): ").lower()
        if player_choice == "да":
            player_card_suit, player_card_rank = deal_card()
            player_score += card_value(player_card_rank)
            print("Вы получили карту:", player_card_rank, player_card_suit)
            print("Сумма ваших карт:", player_score)

            if player_score > 21:
                print("Перебор! У вас больше 21. You got no money bitch")
                return
        else:
            print("Тормозиииим")

            # Ход дилера
            print("Карты дилера:", dealer_card1_rank, dealer_card1_suit, "и", dealer_card2_rank, dealer_card2_suit)
            print("Сумма карт дилера:", dealer_score)

            while dealer_score < 17:
                dealer_card_suit, dealer_card_rank = deal_card()
                dealer_score += card_value(dealer_card_rank)
                print("Дилер получил карту:", dealer_card_rank, dealer_card_suit)
                print("Сумма карт дилера:", dealer_score)

            # ПРОВЕРОЧКА
            if dealer_score > 21:
                print("У дилера перебор! FLAWLESS VICTORY")
            elif dealer_score > player_score:
                print("У дилера больше очков. You got no money bitch")
            elif dealer_score < player_score:
                print("У вас больше очков. YOU WIN")
            else:
                print("Ничья! У вас и у дилера одинаковое количество очков.")

            return


game()