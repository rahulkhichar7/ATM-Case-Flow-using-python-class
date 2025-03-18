import json
from datetime import datetime

class ATM:
    def __init__(self):
        self.current_user = None
        self.balance = 0 
        try:
            with open("users.json",'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users={}
        except json.JSONDecodeError:
            self.users={}
    
    def save_user(self):
        with open('users.json','w') as f:
            json.dump(self.users, f, indent=4)
        
    def create_account(self):
        print("\n--- Create Account ---")
        while True:
            username = input("Enter new username: ")
            if username in self.users:
                print("Username already exists. Please choose a different one.")
            else:
                password = input("Enter password: ")
                confirm_password = input("Confirm password: ")
                if password == confirm_password:
                    # Security questions setup
                    security_questions = []
                    for i in range(4):
                        question = input(f"Choose security question {i + 1} (e.g., 'What is your favorite color?'): ")
                        answer = input("Provide an answer: ")
                        security_questions.append((question, answer))  # Store as a tuple

                    # Save user data
                    self.users[username] = {
                        'password': password,
                        'balance': 0,
                        'transactions': [],
                        'security_questions': security_questions  # List of tuples for questions and answers
                    }
                    print(f"Account created successfully for {username}!")
                    self.save_user()
                    break
                else:
                    print("Passwords do not match. Try again.")


    def login(self):
        print("\n--- Login ---")
        while True:
            username = input("Enter your username: ")
            if username in self.users:
                password = input("Enter your password: ")
                if self.users[username]['password'] == password:
                    self.current_user = username
                    self.balance = self.users[username]['balance']
                    print(f"Welcome, {username}!")
                    return True
                else:
                    print("Incorrect password. Try again.")
            else:
                print("Username not found. Please try again or create a new account.")
                return False

    def check_balance(self):
        print(f"Your current balance is: ${self.balance}")
        

    def change_or_recover_password(self):
        print("\n--- Change or Recover Password ---")
        choice = input("Do you want to (1) Change your password or (2) Reset your password? (Enter 1 or 2): ")

        if choice == '1':
            current_password = input("Enter your current password: ")
            if self.users[self.current_user]['password'] == current_password:
                new_password = input("Enter new password: ")
                confirm_password = input("Confirm new password: ")
                if new_password == confirm_password:
                    self.users[self.current_user]['password'] = new_password
                    self.save_user()
                    print("Password changed successfully!")
                else:
                    print("New passwords do not match.")
            else:
                print("Incorrect current password.")

        elif choice == '2':
            # Password recovery flow
            username = input("Enter your username: ")
            if username in self.users:
                security_questions = self.users[username]['security_questions']
                correct_answers = 0

                for i, (question, answer) in enumerate(security_questions):
                    user_answer = input(f"Security Question {i + 1}: {question}\nYour answer: ")
                    if user_answer.strip().lower() == answer.strip().lower():
                        correct_answers += 1
                    else:
                        print("Incorrect answer. Unable to recover the password.")
                        return
                
                if correct_answers == 4:
                    print(f"All answers are correct! Your password is: {self.users[username]['password']}")
                else:
                    print("You did not answer all questions correctly. Password recovery failed.")
            else:
                print("Username not found.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

    
    def transfer_funds(self):
        recipient = input("Enter the recipient's username: ")
        if recipient in self.users:
            amount = float(input("Enter the amount to transfer: "))
            if amount > 0 and amount <= self.balance:
                self.balance -= amount
                self.users[recipient]['balance'] += amount
                self.users[self.current_user]['transactions'].append({'type': f'Transfer Moeny to {recipient}',
                                                                    'amount': amount,
                                                                    'balance': self.balance,
                                                                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                self.users[recipient]['transactions'].append({'type': f'Recived money from {self.current_user}',
                                                                    'amount': amount,
                                                                    'balance': self.balance,
                                                                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                self.save_user()
                print(f"Successfully transferred ${amount} to {recipient}.")
            else:
                print("Invalid transfer amount.")
        else:
            print("Recipient not found.")
            
    def submit_feedback(self):
        feedback = input("Please enter your feedback: ")
        with open('feedback.txt', 'a') as f:
            f.write(f"{self.current_user}: {feedback}\n")
        print("Thank you for your feedback!")


    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.users[self.current_user]['balance'] = self.balance  
            self.users[self.current_user]['transactions'].append({'type': 'Deposit',
                                                                    'amount': amount,
                                                                    'balance': self.balance,
                                                                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            self.save_user()
            print(f"Successfully deposited ${amount}. Your new balance is: ${self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            self.users[self.current_user]['balance'] = self.balance  
            self.users[self.current_user]['transactions'].append({'type': 'Deposit',
                                                                    'amount': amount,
                                                                    'balance': self.balance,
                                                                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            self.save_user()
            print(f"Successfully withdrew ${amount}. Your new balance is: ${self.balance}")

    def atm_menu(self):
        while True:
            print("\n--- ATM Menu ---")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check transition details")
            print("5. Change/reset Password")
            print("6. Transfer money")
            print("7. Give Feedback")
            print("8. Exit")
            

            choice = input("Choose an option: ")  

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                amount = float(input("Enter the deposit amount: "))
                self.deposit(amount)
            elif choice == '3':
                amount = float(input("Enter the withdrawal amount: "))
                self.withdraw(amount)
            elif choice =='4':
                for i in self.users[self.current_user]['transactions']:
                    print(f"{i['type']}:${i['amount']} on {i['timestamp']} balance: ${i['balance']}")
                print(f"Current Balance ${self.balance}")
            elif choice =='5':
                self.change_or_recover_password()
            elif choice =='6':
                self.transfer_funds()
            elif choice =='7':
                self.submit_feedback()
            elif choice == '8':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option. Please choose a valid option.")

    def start(self):
        print("Welcome to the ATM!")
        while True:
            print("\n1. Already have an account, login")
            print("2. Create Account")
            choice = input("Enter your choice (1 for login, 2 for create account): ")  
            if choice == '1':  
                if self.login():
                    self.atm_menu()
                    break
            elif choice == '2':  
                self.create_account()
            else:
                print("Invalid choice, please type '1' or '2'.")

# Main flow
atm = ATM()
atm.start()
