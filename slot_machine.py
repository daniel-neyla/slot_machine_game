import random

MIN_BET = 5
MAX_BET = 100
MAX_DEPOSIT = 1000
ROWS = 3
COLOUMNS = 3
MAX_LINES = 3


symbols_and_payouts = {
    "Cherry": (0.3, 2),  # Cherry has a 30% probability and a payout rate of 2.
    "Lemon": (0.2, 3),  # Lemon has a 20% probability and a payout rate of 3.
    "Orange": (0.15, 5),  # Orange has a 15% probability and a payout rate of 5.
    "Plum": (0.1, 10),  # Plum has a 10% probability and a payout rate of 10.
    "Bell": (0.1, 10),  # Bell has a 10% probability and a payout rate of 10.
    "Bar": (0.1, 20),  # Bar has a 10% probability and a payout rate of 20.
    "Seven": (0.05, 50),  # Seven has a 5% probability and a payout rate of 50.
}

symbols = list(symbols_and_payouts.keys())
probabilities = [value[0] for value in symbols_and_payouts.values()]

longest_symbol = max(symbols, key=len)


def check_vertical(reels, bet):
    prize_money = 0
    for row in reels:
        if all(symbol == row[0] for symbol in row):
            prize_money += bet * symbols_and_payouts[row[0]][1]
    return prize_money


def check_horizontal(reels, bet):
    prize_money = 0
    for s1, s2, s3 in zip(*reels):
        if s1 == s2 == s3:
            prize_money += bet * symbols_and_payouts[s1][1]

    return prize_money


def check_diagonal(reels, bet):
    prize_money = 0
    first_row, second_row, third_row = reels[0], reels[1], reels[2]

    if first_row[0] == second_row[1] == third_row[2]:
        prize_money += bet * symbols_and_payouts[first_row[0]][1]

    if first_row[2] == second_row[1] == third_row[0]:
        prize_money += bet * symbols_and_payouts[third_row[0]][1]

    return prize_money


class SlotMachine:
    def __init__(self):
        self.balance = 0
        self.current_bet = 0
        self.lines = 1
        self.reels = [symbols] * ROWS

    def get_valid_input(self, prompt, min_value, max_value):
        while True:
            try:
                value = int(input(prompt))
                if not min_value <= value <= max_value:
                    print(f"Value has to be between {min_value} and {max_value}")
                else:
                    return value
            except ValueError:
                print("Enter a valid number")

    def deposit(self):
        amount = self.get_valid_input(
            "How much do you want to deposit? ", 1, MAX_DEPOSIT
        )
        print(
            "You have successfully deposited {amount}$ to your balance".format(
                amount=amount
            )
        )
        self.balance += amount

    def bet(self):
        if self.balance == 0:
            print("You cannot place a bet when your balance is 0")
            return

        lines = self.get_valid_input(
            f"On how many lines do you want to bet(1-{MAX_LINES})? ", 1, MAX_LINES
        )

        self.lines = lines

        amount = self.get_valid_input(
            "How much do you want to bet on each line? ", MIN_BET, MAX_BET
        )

        bet = amount * lines

        if bet >= self.balance:
            print(
                f"Bet cannot be bigger than your current balance, which is {self.balance}"
            )
        else:
            print(f"Your bet is set at {bet}$")
            self.current_bet = bet

    def withdraw(self):
        amount = self.balance
        self.balance = 0
        print(
            "You have withdrawn {amount}$, congrats! Your balance is now set to {balance}$".format(
                amount=amount, balance=self.balance
            )
        )

    def spin(self):
        if self.current_bet <= self.balance:
            self.balance -= self.current_bet
            spins = [
                random.choices(reel, weights=probabilities, k=COLOUMNS)
                for reel in self.reels
            ]

            for i in range(3):
                padded_symbols = [spin.ljust(len(longest_symbol)) for spin in spins[i]]
                print("|".join(padded_symbols))

            total_win = 0
            if self.lines >= 1:
                total_win += check_horizontal(spins, self.current_bet)
            if self.lines >= 2:
                total_win += check_vertical(spins, self.current_bet)
            if self.lines == 3:
                total_win += check_diagonal(spins, self.current_bet)

            self.balance += total_win
            print(f"You won {total_win}$ and your total balance is {self.balance}$")

        else:
            print(
                f"You do not have enough money to place this bet. Your current balance is {self.balance}"
            )


# Usage

slot_machine = SlotMachine()


def game():
    user_choices = {
        1: slot_machine.deposit,
        2: slot_machine.bet,
        3: slot_machine.spin,
        4: slot_machine.withdraw,
        5: "exit",
    }
    while True:
        print(
            "\n1. Make a deposit\n2. Place a bet\n3. Spin\n4. Withdraw the money\n5. Stop playing"
        )
        choice = input("What do you want to do(1-5)? ")
        if choice.isdigit():
            choice = int(choice)
            if choice in user_choices:
                if user_choices[choice] == "exit":
                    break
                else:
                    user_choices[choice]()
            else:
                print("This is not a valid choice")
        else:
            print("Enter a valid number")


game()
