import random

MIN_BET = 5
MAX_BET = 100
MAX_DEPOSIT = 1000


class SlotMachine:
    def __init__(self):
        self.balance = 0
        self.current_bet = 0

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
        self.balance += amount

    def bet(self):
        amount = self.get_valid_input("How much do you want to bet? ", MIN_BET, MAX_BET)
        if amount > self.balance:
            print(
                f"Bet cannot be bigger than your current balance, which is {self.balance}"
            )
        else:
            self.current_bet += amount

    def withdraw(self):
        amount = self.balance
        self.balance = 0
        print(
            "You have withdrawn {amount}. It is now set to {balance}".format(
                amount=amount, balance=self.balance
            )
        )

    def spin(self):
        return


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
            "1. Make a deposit\n2. Place a bet\n3. Spin\n4. Withdraw the money\n5. Stop playing"
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
