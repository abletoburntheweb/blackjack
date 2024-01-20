import random

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def play_game():
    player_score = 0
    bot_score = 0

    while player_score <= 21 and bot_score <= 21:

        start = input("Нажмите Enter, чтобы взять карту...")
        while start == "":
            print("=====================================")
            player_card = deal_card()
            print(f"Вы взяли {player_card}.")
            player_score += player_card
            print("=====================================")
            input("Нажмите Enter, чтобы бот взял карту...")
            print("=====================================")
            bot_card = deal_card()
            print(f"Бот взял {bot_card}.")
            bot_score += bot_card
            print("=====================================")
            print(f"Ваш текущий счёт: {player_score}.")
            print(f"Счёт бота: {bot_score}.")
            print("=====================================")
            start == 1
            if player_score == bot_score:
                start = input("Ничья!")
            elif bot_score == 0:
                start = input("Вы проиграли! У дилера Blackjack!")
            elif player_score == 0:
                start = input("Поздравляю! У вас Blackjack!")
            elif player_score > 21:
                start = input("Вы проиграли! Перебор!")
            elif bot_score > 21:
                start = input("Поздравляю! Дилер перебрал, вы выиграли!")
            elif player_score > bot_score:
                start = input("Поздравляю! Вы победили!")
            elif player_score and bot_score > 21:
                start = input("Ничья!")
            else:
                start = input("Вы проиграли!")
    else:
        input("Прощайте!")

play_game()