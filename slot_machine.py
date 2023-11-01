import random
from rich import print
from rich.console import Console
from rich.theme import Theme
from pyfiglet import Figlet

custom_theme = Theme({"info": "dim cyan", "warning": "magenta", "win": "bold green"})
console = Console(theme=custom_theme)

f = Figlet(font="slant")


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

symbol_colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
symbols = list(symbols_and_payouts.keys())
symbol_to_color = {symbol: color for symbol, color in zip(symbols, symbol_colors)}


probabilities = [value[0] for value in symbols_and_payouts.values()]

longest_symbol = max(symbols, key=len)


def check_wins(reels, bet, horizontal=False, vertical=False, diagonal=False):
    prize_money = 0
    if horizontal:
        for s1, s2, s3 in zip(*reels):
            if s1 == s2 == s3:
                prize_money += bet * symbols_and_payouts[s1][1]
    if vertical:
        for row in reels:
            if all(symbol == row[0] for symbol in row):
                prize_money += bet * symbols_and_payouts[row[0]][1]

    if diagonal:
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
                    console.print(
                        f"[warning]Value has to be between {min_value} and {max_value}[/warning]"
                    )
                else:
                    return value
            except ValueError:
                console.print("[warning]Enter a valid number[\warning]")

    def deposit(self):
        amount = self.get_valid_input(
            "How much do you want to deposit? ", 1, MAX_DEPOSIT
        )

        self.balance += amount

        console.print(
            f"\n[info]You have successfully deposited ${amount} to your balance. Your current balance is ${self.balance}.[/info]\n"
        )

    def bet(self):
        if self.balance == 0:
            console.print(
                "\n[warning]You cannot place a bet when your balance is 0[/warning]"
            )
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
            console.print(
                f"\n[warning]Bet cannot be bigger than your current balance, which is {self.balance}[/warning]"
            )
        else:
            console.print(f"\n[info]Your bet is set at {bet}$\n[/info]")
            self.current_bet = bet

    def withdraw(self):
        amount = self.balance
        self.balance = 0
        self.bet = 0
        self.lines = 1
        if amount == 0:
            console.print(
                "\n[warning]You cannot withdraw any money because your balance is 0$[/warning]\n"
            )
        else:
            console.print(
                "\n[win]You have withdrawn {amount}$, congrats! Your balance is now set to {balance}$[/win]\n".format(
                    amount=amount, balance=self.balance
                )
            )

    def spin(self):
        if self.current_bet == 0:
            console.print("[warning]You first need to bet some money[/warning]")

        elif self.current_bet <= self.balance:
            self.balance -= self.current_bet
            spins = [
                random.choices(reel, weights=probabilities, k=COLOUMNS)
                for reel in self.reels
            ]

            print("\n")
            print("+", "-" * len(longest_symbol) * 3, "+")
            for i in range(3):
                padded_symbols = [spin.ljust(len(longest_symbol)) for spin in spins[i]]

                for symbol in padded_symbols:
                    console.print(
                        symbol, style=f"bold {symbol_to_color[symbol.strip()]}", end=""
                    )
                    console.print("|", style="bold white", end="")
                console.print()  # Print newline at the end of each row
            print("+", "-" * len(longest_symbol) * 3, "+")

            total_win = 0
            if self.lines >= 1:
                total_win += check_wins(spins, self.current_bet, True)
            if self.lines >= 2:
                total_win += check_wins(spins, self.current_bet, True, True)
            if self.lines == 3:
                total_win += check_wins(spins, self.current_bet, True, True, True)

            self.balance += total_win
            console.print(
                f"\n[win]You won {total_win}$ and your total balance is {self.balance}$[/win]\n"
            )

        else:
            console.print(
                f"\n[warning]You do not have enough money to place this bet. Your current balance is {self.balance}[/warning]"
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
    print(f.renderText("Welcome!"))
    while True:
        print("[bold cyan]\nHere are your options:")
        options = [
            "Make a deposit",
            "Place a bet",
            "Spin",
            "Withdraw the money",
            "Stop playing",
        ]
        for i, option in enumerate(options, 1):
            print(f"[bold yellow]{i}. [bold green]{option}")
        choice = input("\nWhat do you want to do (1-5)? ")
        if choice.isdigit():
            choice = int(choice)
            if choice in user_choices:
                if user_choices[choice] == "exit":
                    if slot_machine.balance > 0:
                        while True:
                            player_exit = input(
                                "If you exit the game now, all your money will be gone. Exit(Y/N)? "
                            )
                            if player_exit in ["y", "Y", "n", "N"]:
                                break

                            else:
                                console.print("[warning]Not a valid response[/warning]")
                        if player_exit in ["Y", "y"]:
                            break
                    else:
                        break
                else:
                    user_choices[choice]()
            else:
                print("This is not a valid choice")
        else:
            print("Enter a valid number")


game()
