import random

MIN_BET = 5
MAX_BET = 100
MAX_DEPOSIT = 1000
ROWS = 3
COLOUMNS = 3
MAX_LINES = 3

symbols_and_probabilities = {
    "Cherry": 0.3,
    "Lemon": 0.2,
    "Orange": 0.15,
    "Plum": 0.1,
    "Bell": 0.1,
    "Bar": 0.1,
    "Seven": 0.05,
}
symbols = list(symbols_and_probabilities.keys())
probabilities = list(symbols_and_probabilities.values())
longest_symbol = max(symbols, key=len)


def check_vertical(reels):
    count = 0
    for row in reels:
        if all(symbol == row[0] for symbol in row):
            count += 1
    return count


def check_horizontal(reels):
    count = 0
    for s1, s2, s3 in zip(*reels):
        if s1 == s2 == s3:
            count += 1

    return count


def check_diagonal(reels):
    count = 0
    first_row, second_row, third_row = reels[0], reels[1], reels[2]

    if first_row[0] == second_row[1] == third_row[2]:
        count += 1

    if first_row[2] == second_row[1] == third_row[0]:
        count += 1

    return count


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
            f"On how many lines do you want to bet(1-{MAX_LINES})?", 1, MAX_LINES
        )

        self.lines = lines

        amount = self.get_valid_input(
            "How much do you want to bet on each line? ", MIN_BET, MAX_BET
        )

        bet = amount * lines

        if bet > self.balance:
            print(
                f"Bet cannot be bigger than your current balance, which is {self.balance}"
            )
        else:
            print(f"Your bet is set at {bet}")
            self.current_bet += bet

    def withdraw(self):
        amount = self.balance
        self.balance = 0
        print(
            "You have withdrawn {amount}. It is now set to {balance}".format(
                amount=amount, balance=self.balance
            )
        )

    def spin(self):
        if self.current_bet < self.balance:
            spins = [
                random.choices(reel, weights=probabilities, k=COLOUMNS)
                for reel in self.reels
            ]

            print(spins)
            for i in range(3):
                padded_symbols = [spin.ljust(len(longest_symbol)) for spin in spins[i]]
                print("|".join(padded_symbols))

            wins = 0
            if self.lines == 3:
                wins += check_diagonal(spins)
                wins += check_horizontal(spins)
                wins += check_vertical(spins)

            print(wins)


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
