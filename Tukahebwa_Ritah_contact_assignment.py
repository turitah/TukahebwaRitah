def valid_phone(phone_number):
    for character in phone_number:
        if not (character.isdigit() or character == "-" or character == "+"):
            return False
    return True


def valid_email(email):
    if "@" in email and "." in email:
        return True
    return False


def main():

    contacts = []

    while True:

        print("\n== Contact Manager Menu ==")
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")

        # Add Contact
        if choice == "1":

            name = input("Enter name: ")
            phone_number = input("Enter phone number: ")
            email = input("Enter email: ")

            if valid_email(email):

                if valid_phone(phone_number):

                    contacts.append([name, phone_number, email])

                    print("Contact saved successfully")

                else:
                    print("Invalid phone number")

            else:
                print("Invalid email")

        # View Contact
        elif choice == "2":

            name = input("Enter contact name: ")

            found = False

            for contact in contacts:

                if contact[0] == name:

                    print("\nContact Found")
                    print("Name:", contact[0])
                    print("Phone Number:", contact[1])
                    print("Email:", contact[2])

                    found = True

            if not found:
                print("Contact not found")

        # Update Contact
        elif choice == "3":

            name = input("Enter contact name to update: ")

            found = False

            for contact in contacts:

                if contact[0] == name:

                    new_phone_number = input("Enter new phone number: ")
                    new_email = input("Enter new email: ")

                    if valid_email(new_email):

                        if valid_phone(new_phone_number):

                            contact[1] = new_phone_number
                            contact[2] = new_email

                            print("Contact updated successfully")

                        else:
                            print("Invalid phone number")

                    else:
                        print("Invalid email")

                    found = True

            if not found:
                print("Contact not found")

        # Delete Contact
        elif choice == "4":

            name = input("Enter contact name to delete: ")

            found = False

            for contact in contacts:

                if contact[0] == name:

                    contacts.remove(contact)

                    print("Contact successfully deleted")

                    found = True
                    break

            if not found:
                print("Contact not found")

        # Search Contacts
        elif choice == "5":

            search = input("Enter name, phone number or email to search: ")

            found = False

            for contact in contacts:

                if search in contact:

                    print("\nContact Found")
                    print("Name:", contact[0])
                    print("Phone Number:", contact[1])
                    print("Email:", contact[2])

                    found = True

            if not found:
                print("Contact not found")

        # List All Contacts
        elif choice == "6":

            if len(contacts) == 0:

                print("No contacts available.")

            else:

                print("\n== All Contacts ==")

                for contact in contacts:

                    print("-------------------")
                    print("Name:", contact[0])
                    print("Phone Number:", contact[1])
                    print("Email:", contact[2])

        # Exit
        elif choice == "7":

            print("Thank you so much")
            break

        else:

            print("Invalid option. Please choose between 1 and 7.")


main()