import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox

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


class BlackjackWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blackjack PyQt5")
        self.setGeometry(100, 100, 500, 600)

        self.player_balance = 100
        self.bet_amount = 0
        self.player_hand = []
        self.dealer_hand = []
        self.split_hand = []  # Для хранения второй руки при сплите
        self.is_split = False  # Флаг для отслеживания, произошел ли сплит
        self.player_scores = [0]  # Список для хранения очков для каждой руки
        self.dealer_score = 0
        self.current_hand = 0  # Индекс текущей руки игрока

        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.balance_label = QLabel(f"Balance: {self.player_balance}", self)
        self.bet_label = QLabel("Bet amount:", self)
        self.bet_input = QLineEdit(self)
        self.bet_button = QPushButton("Place Bet", self)
        self.bet_button.clicked.connect(self.place_bet)

        self.deal_button = QPushButton("Deal", self)
        self.deal_button.clicked.connect(self.deal)
        self.deal_button.setEnabled(False)

        self.hit_button = QPushButton("Hit", self)
        self.hit_button.clicked.connect(self.hit)
        self.hit_button.setEnabled(False)

        self.stand_button = QPushButton("Stand", self)
        self.stand_button.clicked.connect(self.stand)
        self.stand_button.setEnabled(False)

        self.double_button = QPushButton("Double Down", self)
        self.double_button.clicked.connect(self.double_down)
        self.double_button.setEnabled(False)

        self.split_button = QPushButton("Split", self)
        self.split_button.clicked.connect(self.split)
        self.split_button.setEnabled(False)

        self.player_hand_label = QLabel("Your hands:", self)
        self.dealer_hand_label = QLabel("Dealer's hand:", self)

        layout = QVBoxLayout()
        bet_hbox = QHBoxLayout()

        bet_hbox.addWidget(self.bet_label)
        bet_hbox.addWidget(self.bet_input)
        bet_hbox.addWidget(self.bet_button)

        layout.addWidget(self.balance_label)
        layout.addLayout(bet_hbox)
        layout.addWidget(self.deal_button)
        layout.addWidget(self.player_hand_label)
        layout.addWidget(self.dealer_hand_label)
        layout.addWidget(self.hit_button)
        layout.addWidget(self.stand_button)
        layout.addWidget(self.double_button)
        layout.addWidget(self.split_button)

        self.central_widget.setLayout(layout)

    def place_bet(self):
        try:
            self.bet_amount = int(self.bet_input.text())
            if self.bet_amount <= 0 or self.bet_amount > self.player_balance:
                QMessageBox.warning(self, 'Invalid Bet', "Enter a positive number no greater than your balance.")
            else:
                self.player_balance -= self.bet_amount
                self.update_balance_label()
                self.deal_button.setEnabled(True)
                self.bet_button.setEnabled(False)
        except ValueError:
            QMessageBox.warning(self, 'Invalid Input', "Please enter a numeric value.")

    def update_balance_label(self):
        self.balance_label.setText(f"Balance: {self.player_balance}")

    def update_hand_labels(self):
        player_hand_str = ' '.join([f"{card[1]}{card[0]}" for card in self.player_hand])
        split_hand_str = ' '.join([f"{card[1]}{card[0]}" for card in self.split_hand]) if self.is_split else ""
        dealer_hand_str = ' '.join([f"{card[1]}{card[0]}" for card in self.dealer_hand[:-1]]) + " ??" if self.dealer_hand else ""

        self.player_hand_label.setText(f"Your hand: {player_hand_str}\nSplit hand: {split_hand_str} (Score: {self.player_scores})")
        self.dealer_hand_label.setText(f"Dealer's hand: {dealer_hand_str}")

    def deal(self):
        self.player_hand = [deal_card(), deal_card()]
        self.dealer_hand = [deal_card(), deal_card()]
        self.player_scores = [card_value(self.player_hand[0][1], 0) + card_value(self.player_hand[1][1], 0)]
        self.dealer_score = card_value(self.dealer_hand[0][1], 0) + card_value(self.dealer_hand[1][1], 0)

        self.update_hand_labels()
        self.check_split_double()

    def check_split_double(self):
        # Проверяем возможность сплита и дабла
        self.deal_button.setEnabled(False)
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.double_button.setEnabled(self.player_balance >= self.bet_amount)
        self.split_button.setEnabled(self.player_hand[0][1] == self.player_hand[1][1] and self.player_balance >= self.bet_amount)

    def hit(self):
        if self.current_hand > len(self.player_scores) - 1:  # Если текущая рука больше чем список очков, игра окончена
            return

        new_card = deal_card()
        self.player_hand.append(new_card)
        self.player_scores[self.current_hand] += card_value(new_card[1], self.player_scores[self.current_hand])

        self.update_hand_labels()
        self.double_button.setEnabled(False)
        self.split_button.setEnabled(False)

        if self.player_scores[self.current_hand] > 21:
            QMessageBox.information(self, 'Bust!', "You've busted!")
            self.current_hand += 1
            if self.current_hand > len(self.player_scores) - 1:
                self.stand()  # Если это была последняя рука, переходим к дилеру

    def stand(self):
        self.current_hand += 1
        if self.current_hand > len(self.player_scores) - 1:
            while self.dealer_score < 17:
                new_card = deal_card()
                self.dealer_hand.append(new_card)
                self.dealer_score += card_value(new_card[1], self.dealer_score)

            self.dealer_hand_label.setText(f"Dealer's hand: {' '.join([f'{card[1]}{card[0]}' for card in self.dealer_hand])} (Score: {self.dealer_score})")

            self.check_winner()

    def double_down(self):
        if self.player_balance < self.bet_amount:
            QMessageBox.warning(self, 'Invalid Action', "Not enough balance to double down.")
            return

        self.player_balance -= self.bet_amount
        self.bet_amount *= 2
        self.hit()
        if self.player_scores[self.current_hand] <= 21:
            self.stand()

    def split(self):
        if not self.player_hand[0][1] == self.player_hand[1][1]:
            QMessageBox.warning(self, 'Invalid Action', "You can only split when you have a pair.")
            return

        if self.player_balance < self.bet_amount:
            QMessageBox.warning(self, 'Invalid Action', "Not enough balance to split.")
            return

        self.player_balance -= self.bet_amount
        self.split_hand = [self.player_hand.pop()]
        self.player_hand.append(deal_card())
        self.split_hand.append(deal_card())
        self.player_scores.append(card_value(self.split_hand[0][1], 0) + card_value(self.split_hand[1][1], 0))
        self.is_split = True

        self.update_hand_labels()
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.double_button.setEnabled(False)
        self.split_button.setEnabled(False)

    def check_winner(self):
        for score in self.player_scores:
            if score > 21:
                QMessageBox.information(self, 'Bust!', "You've busted!")
            elif self.dealer_score > 21 or score > self.dealer_score:
                QMessageBox.information(self, 'Winner!', "You win!")
                self.player_balance += self.bet_amount * 2
            elif self.dealer_score > score:
                QMessageBox.information(self, 'Loser!', "Dealer wins!")
            else:
                QMessageBox.information(self, 'Push!', "It's a tie!")
                self.player_balance += self.bet_amount

        self.update_balance_label()
        self.end_round()

    def end_round(self):
        self.bet_button.setEnabled(True)
        self.deal_button.setEnabled(False)
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.double_button.setEnabled(False)
        self.split_button.setEnabled(False)
        self.bet_input.clear()
        self.player_hand = []
        self.dealer_hand = []
        self.split_hand = []
        self.is_split = False
        self.player_scores = [0]
        self.current_hand = 0

        if self.player_balance <= 0:
            QMessageBox.warning(self, 'Game Over', "You've run out of money!")
            QApplication.instance().quit()

    # ... Остальные методы


def main():
    app = QApplication(sys.argv)
    window = BlackjackWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()