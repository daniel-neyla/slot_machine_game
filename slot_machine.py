import random


class SlotMachine:
    def __init__(self):
        self.balance = 0

    def deposite(self):
        while True:
            try:
                deposite = int(input("How much do you want to bet? "))
                if deposite > 0 and deposite <= 20:
                    self.balance += deposite
                    break
                else:
                    print("Deposite has to be between 0 and 21")
            except ValueError:
                print("You have to enter a valid number")


# Usage
slot_machine = SlotMachine()
