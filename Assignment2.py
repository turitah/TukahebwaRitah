max_attempts = 3
attempts = 0
logged_in = False

while attempts < max_attempts:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username == "Admin" and password == "admin256":
        print("Welcome Admin! You have full access.")
        logged_in = True
        break

    elif username == "Customer" and password == "customer123":
        print("Welcome Customer! You have limited access.")
        logged_in = True
        break

    elif username == "Cashier" and password == "cashier789":
        print("Welcome Cashier! Can process customer sales.")
        logged_in = True
        break

    else:
        attempts += 1
        print("Invalid username or password.")

if logged_in:

    # E-commerce calculator  
    sub_total = float(input("Enter product price: "))
    coupon_code = input("Enter coupon code: ")
    location = input("Enter location: ")

    # Discount based on subtotal
    if sub_total >= 40000:
        discount = 20
    elif sub_total >= 20000:
        discount = 10
    else:
        discount = 5

    # Coupon discount
    coupon_discount = 0

    if coupon_code == "SAVE10":
        coupon_discount = 10
    elif coupon_code == "SAVE20":
        coupon_discount = 20
    elif coupon_code == "SAVE30":
        coupon_discount = 30

    total_discount = discount + coupon_discount

    discount_amount = (sub_total * total_discount) / 100
    amount_after_discount = sub_total - discount_amount

    # Tax rate
    if location.lower() == "uganda":
        tax_rate = 16
    elif location.lower() == "kenya":
        tax_rate = 14
    elif location.lower() == "tanzania":
        tax_rate = 12
    else:
        tax_rate = 10

    tax_amount = (amount_after_discount * tax_rate) / 100
    final_price = amount_after_discount + tax_amount

    print("\n===== RECEIPT =====")
    print("Subtotal:", sub_total)
    print("Discount:", total_discount, "%")
    print("Tax Rate:", tax_rate, "%")
    print("Final Price:", final_price)

else:
    print("Failed login attempts. Please try again later.")