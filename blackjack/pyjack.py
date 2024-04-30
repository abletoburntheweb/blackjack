import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout,  QHBoxLayout, QWidget, QMessageBox

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
        self.player_score = 0
        self.dealer_score = 0

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

        self.player_hand_label = QLabel("Your hand:", self)
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
        dealer_hand_str = ' '.join([f"{card[1]}{card[0]}" for card in self.dealer_hand[:-1]]) + " ??"
        self.player_hand_label.setText(f"Your hand: {player_hand_str} (Score: {self.player_score})")
        self.dealer_hand_label.setText(f"Dealer's hand: {dealer_hand_str}")

    def deal(self):
        self.player_hand = [deal_card(), deal_card()]
        self.dealer_hand = [deal_card(), deal_card()]

        self.player_score = sum([card_value(card[1], 0) for card in self.player_hand])
        self.dealer_score = sum([card_value(card[1], 0) for card in self.dealer_hand])

        self.update_hand_labels()

        self.deal_button.setEnabled(False)
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)

    def hit(self):
        new_card = deal_card()
        self.player_hand.append(new_card)
        self.player_score += card_value(new_card[1], self.player_score)

        self.update_hand_labels()

        if self.player_score > 21:
            QMessageBox.information(self, 'Bust!', "You've busted!")
            self.end_round()

    def stand(self):
        while self.dealer_score < 17:
            new_card = deal_card()
            self.dealer_hand.append(new_card)
            self.dealer_score += card_value(new_card[1], self.dealer_score)

        dealer_hand_str = ' '.join([f"{card[1]}{card[0]}" for card in self.dealer_hand])
        self.dealer_hand_label.setText(f"Dealer's hand: {dealer_hand_str} (Score: {self.dealer_score})")

        self.check_winner()

    def check_winner(self):
        if self.dealer_score > 21 or self.player_score > self.dealer_score:
            QMessageBox.information(self, 'Winner!', "You win!")
            self.player_balance += self.bet_amount * 2
        elif self.dealer_score > self.player_score:
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
        self.bet_input.clear()

        if self.player_balance <= 0:
            QMessageBox.warning(self, 'Game Over', "You've run out of money!")
            QApplication.instance().quit()


def main():
    app = QApplication(sys.argv)
    window = BlackjackWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()