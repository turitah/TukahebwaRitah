Day = int(input("Enter the  Day between (1-7): "))
match Day:
    case 1:
        print("its Monday")
    case 2:
        print("its Tuesday")
    case 3:
        print("its Wednesday")
    case 4:
        print("its Thurday")
    case 5:
        print("its Friday")
    case 6:
        print("its Saturday")
    case 7:
        print("its Sunday")
    case _:
        print("Invalid Day. Please enter the Day between 1 and 7")
   