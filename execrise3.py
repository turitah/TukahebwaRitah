balance = 1000

while balance > 0:

    print(f"\nCurrent balance: ${balance}")

    action = input(
        "Do you want to deposit or withdraw? (deposit/withdraw): "
    ).lower()

    if action == "deposit":

        amount = float(input("Enter the amount to deposit: "))

        balance += amount

        print(f"You deposited ${amount}.")

    elif action == "withdraw":

        amount = float(input("Enter the amount to withdraw: "))

        if amount > balance:
            print("Insufficient funds. You cannot withdraw that amount.")

        else:
            balance -= amount
            print(f"You withdrew ${amount}.")

    else:
        print("Invalid action. Please enter 'deposit' or 'withdraw'.")