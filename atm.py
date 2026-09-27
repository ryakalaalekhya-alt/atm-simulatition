import sys
import time

class Account:
    def __init__(self, pin, balance=0.0):
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def verify_pin(self, entered_pin):
        return self.pin == entered_pin

    def log_transaction(self, activity):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"[{timestamp}] {activity}")

class ATMMachine:
    def __init__(self):
        # Database containing Mock Data: Card Number mapping to Account objects
        self.accounts_db = {
            "123456": Account(pin="1111", balance=1500.00),
            "789012": Account(pin="2222", balance=500.50),
            "987654": Account(pin="3333", balance=25000.00)
        }
        self.current_account = None
        self.current_card = None

    def start(self):
        print("=" * 40)
        print("       WELCOME TO THE TERMINAL ATM      ")
        print("=" * 40)
        
        if not self.authenticate_user():
            print("\n[Error] Too many invalid attempts. Card retained for security.")
            sys.exit()
            
        self.show_main_menu()

    def authenticate_user(self):
        card_number = input("\nPlease insert/enter your Card Number: ").strip()
        if card_number not in self.accounts_db:
            print("[Error] Unrecognized card number.")
            return False

        account = self.accounts_db[card_number]
        attempts = 3
        
        while attempts > 0:
            entered_pin = input(f"Enter your 4-digit PIN ({attempts} attempts left): ").strip()
            if account.verify_pin(entered_pin):
                self.current_account = account
                self.current_card = card_number
                print("\n[Success] PIN Verified. Access Granted.")
                return True
            else:
                print("[Warning] Invalid PIN.")
                attempts -= 1
                
        return False

    def show_main_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("                MAIN MENU               ")
            print("-" * 40)
            print("1. Check Balance")
            print("2. Deposit Funds")
            print("3. Withdraw Cash")
            print("4. View Statement / History")
            print("5. Exit Session")
            print("-" * 40)
            
            choice = input("Please select an option (1-5): ").strip()
            
            if choice == "1":
                self.check_balance()
            elif choice == "2":
                self.deposit_funds()
            elif choice == "3":
                self.withdraw_cash()
            elif choice == "4":
                self.view_statement()
            elif choice == "5":
                print("\nThank you for choosing our banking services. Goodbye!")
                self.current_account = None
                self.current_card = None
                break
            else:
                print("[Error] Invalid choice. Please pick an option from 1 to 5.")

    def check_balance(self):
        print(f"\n[Balance] Your current balance is: ${self.current_account.balance:,.2f}")

    def deposit_funds(self):
        try:
            amount = float(input("\nEnter the amount to deposit: $"))
            if amount <= 0:
                print("[Error] Deposit amount must be greater than zero.")
                return
            
            self.current_account.balance += amount
            self.current_account.log_transaction(f"Deposited: ${amount:,.2f}")
            print(f"[Success] Successfully deposited ${amount:,.2f}")
            print(f"New Balance: ${self.current_account.balance:,.2f}")
        except ValueError:
            print("[Error] Invalid numeric entry.")

    def withdraw_cash(self):
        try:
            amount = float(input("\nEnter withdrawal amount (Multiples of $10/$20): $"))
            if amount <= 0:
                print("[Error] Withdrawal amount must be greater than zero.")
                return
            if amount % 10 != 0:
                print("[Error] ATM can only dispense multiples of $10 or $20.")
                return
            if amount > self.current_account.balance:
                print("[Error] Insufficient funds available in this account.")
                return

            self.current_account.balance -= amount
            self.current_account.log_transaction(f"Withdrew: ${amount:,.2f}")
            print(f"[Success] Dispensing ${amount:,.2f}...")
            print(f"Remaining Balance: ${self.current_account.balance:,.2f}")
        except ValueError:
            print("[Error] Invalid numeric entry.")

    def view_statement(self):
        print("\n" + "=" * 40)
        print("          TRANSACTION STATEMENT         ")
        print("=" * 40)
        history = self.current_account.transaction_history
        if not history:
            print("No transactions performed during this session.")
        else:
            for log in history:
                print(log)
        print(f"Current Net Balance: ${self.current_account.balance:,.2f}")
        print("=" * 40)

if __name__ == "__main__":
    atm = ATMMachine()
    atm.start()
