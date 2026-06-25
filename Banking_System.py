#parent class
class Transaction:
    def __init__(self, balance):
        self.balance = balance

    def process_transaction(self):
        print("Processing transacation.......")
    def  get_balance(self):
         return self.balance
    
#child class_deposit
class Deposit(Transaction):
#method overriding
    def process_transaction(self):
        print("Deposit transaction processed.")

    def deposit(self, amount, description=None):
        self.balance += amount

        if description:
            print(f"Deposited UGX {amount}")
            print(f"Description: {description}")
        else:
            print(f"Deposited UGX {amount}")
#child class_withdraw
class withdraw(Transaction):

    def process_transaction(self):
        print("withdrawn transaction processed.")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -=amount
            print(f"withdraw UGX {amount}")
        else:
            print("Insufficient balance!")
#child class_Transfer
class Transfer(Transaction):

    def process_transaction(self):
        print("Transfer transaction processed.")

    def transfer(self, amount, recipient):   
        if amount <= self.balance:
            self.balance -= amount
            print(f"Transferred UGX {amount} to {recipient}")
        else:
            print("Insufficient balance!")



print("====EMPLOYER DEPOSIT===")

balance = 0
#depositing money by the employeer
Deposit = Deposit(balance)
Deposit.process_transaction()
amount = float(input("Enter the amount to deposit:"))
Deposit.deposit(amount)
print("Balance:", Deposit.get_balance())

#Withdrawing money
withdraw_obj = withdraw(Deposit.get_balance())
withdraw_obj.process_transaction()

amount = float(input("Enter amount to withdraw: "))
withdraw_obj.withdraw(amount)

print("Balance:", withdraw_obj.get_balance())  

#Transfering money
transfer = Transfer(withdraw_obj.get_balance())    
transfer.process_transaction()

amount = float(input("Enter amount to transfer: "))
recipient = input("Enter recipient name: ")

transfer.transfer(amount, recipient)

print("Final Balance:", transfer.get_balance())

    
         



         
    
     
