import random

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def play_game():
    player_score = 0
    bot_score = 0

    while player_score <= 21 and bot_score <= 21:
        # Ход игрока
        input("Нажмите Enter, чтобы взять карту...")
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

    if player_score == bot_score:
        print("Ничья!")
    elif bot_score == 0:
        print("Вы проиграли! У дилера Blackjack!")
    elif player_score == 0:
        print("Поздравляю! У вас Blackjack!")
    elif player_score > 21:
        print("Вы проиграли! Перебор!")
    elif bot_score > 21: 
        print("Поздравляю! Дилер перебрал, вы выиграли!")
    elif player_score > bot_score:
        print("Поздравляю! Вы победили!")
    elif player_score and bot_score > 21:
        print("Ничья!")
    else:
        print("Вы проиграли!")

play_game()