# STUDENT MANAGEMENT RECORD SYSTEM
import csv
import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "students.csv")
JSON_FILE = os.path.join(BASE_DIR, "students.json")
LOG_FILE = os.path.join(BASE_DIR, "student_system.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class StudentNotFoundError(Exception):
    """Raised when a student cannot be found."""

#csv and json file initialization function
def initialize_files():
    """Create the storage files if they do not already exist."""
    try:
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Registration Number", "Name", "Program"])

        if not os.path.exists(JSON_FILE):
            with open(JSON_FILE, "w", encoding="utf-8") as file:
                json.dump({}, file, indent=4)

        logging.info("Storage files initialized successfully.")
    except Exception as exc:
        logging.error("Failed to initialize files: %s", exc)
        raise

#display menu function
def display_menu():
    """Show the main menu options."""
    print("\n==== STUDENT MANAGEMENT RECORD SYSTEM ====")
    print("1. Add student")
    print("2. View students")
    print("3. Search student")
    print("4. Update student")
    print("5. Delete student")
    print("6. Exit")

#add student function
def add_student():
    """Add a new student to both the CSV and JSON files."""
    try:
        reg = input("Enter Registration Number: ").strip()
        name = input("Enter Name: ").strip()
        program = input("Enter Program: ").strip()
        address = input("Enter Address: ").strip()
        contact = input("Enter Contact: ").strip()

        if not reg:
            raise ValueError("Registration number cannot be empty.")
        if not name:
            raise ValueError("Name cannot be empty.")
        if not program:
            raise ValueError("Program cannot be empty.")
        if not contact.isdigit():
            raise ValueError("Contact must contain only numbers.")

        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        if any(row and row[0] == reg for row in rows[1:]):
            raise ValueError("A student with this registration number already exists.")

        with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([reg, name, program])

        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data[reg] = {
            "Name": name,
            "Address": address,
            "Contact": contact,
            "Program": program
        }

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Student added successfully.")
        logging.info("Added student with registration number %s", reg)

    except ValueError as exc:
        logging.error("Add student failed: %s", exc)
        print(f"Error: {exc}")
    except Exception as exc:
        logging.exception("Unexpected error while adding student: %s", exc)
        print(f"Error: {exc}")
    finally:
        print("Adding a student completed.\n")

#view student function
def view_student():
    """Display all students stored in the CSV file."""
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)

        if len(rows) <= 1:
            print("No students found.")
        else:
            print("\nRegistered students:")
            for row in rows[1:]:
                print(f"Registration: {row[0]} | Name: {row[1]} | Program: {row[2]}")

        logging.info("Viewed all students.")
    except Exception as exc:
        logging.error("Failed to view students: %s", exc)
        print(f"Error: {exc}")
    finally:
        print("Viewing students completed.\n")


def search_student():
    """Search for a student using the registration number."""
    try:
        reg = input("Enter Registration Number: ").strip()

        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        found = False
        for row in rows[1:]:
            if row and row[0] == reg:
                print(f"Found student: Registration: {row[0]} | Name: {row[1]} | Program: {row[2]}")
                found = True
                break

        if not found:
            raise StudentNotFoundError("Student not found.")

        logging.info("Searched for student with registration number %s", reg)
    except StudentNotFoundError as exc:
        logging.error("Search failed: %s", exc)
        print(exc)
    except Exception as exc:
        logging.error("Search failed: %s", exc)
        print(f"Error: {exc}")
    finally:
        print("Searching a student completed.\n")

#update student function
def update_student():
    """Update the information of a student."""
    try:
        reg = input("Enter Registration Number: ").strip()
        new_name = input("Enter new name : ").strip()
        new_program = input("Enter new program : ").strip()
        new_address = input("Enter new address : ").strip()
        new_contact = input("Enter new contact : ").strip()

        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        found = False
        for row in rows[1:]:
            if row and row[0] == reg:
                if new_name:
                    row[1] = new_name
                if new_program:
                    row[2] = new_program
                found = True
                break

        if not found:
            raise StudentNotFoundError("Student not found.")

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Registration Number", "Name", "Program"])
            writer.writerows(rows[1:])

        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if reg in data:
            if new_name:
                data[reg]["Name"] = new_name
            if new_address:
                data[reg]["Address"] = new_address
            if new_contact:
                if not new_contact.isdigit():
                    raise ValueError("Contact must contain only numbers.")
                data[reg]["Contact"] = new_contact
            if new_program:
                data[reg]["Program"] = new_program

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Student updated successfully.")
        logging.info("Updated student with registration number %s", reg)
    except StudentNotFoundError as exc:
        logging.error("Update failed: %s", exc)
        print(exc)
    except ValueError as exc:
        logging.error("Update failed: %s", exc)
        print(f"Error: {exc}")
    except Exception as exc:
        logging.error("Update failed: %s", exc)
        print(f"Error: {exc}")
    finally:
        print("Updating a student completed.\n")

#delete student function
def delete_student():
    """Delete a student record from the CSV and JSON files."""
    try:
        reg = input("Enter Registration Number: ").strip()

        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        updated_rows = []
        found = False
        for row in rows:
            if row and row[0] == reg:
                found = True
            else:
                updated_rows.append(row)

        if not found:
            raise StudentNotFoundError("Student not found.")

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)

        with open(JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.pop(reg, None)

        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print("Student deleted successfully.")
        logging.info("Deleted student with registration number %s", reg)
    except StudentNotFoundError as exc:
        logging.error("Delete failed: %s", exc)
        print(exc)
    except Exception as exc:
        logging.error("Delete failed: %s", exc)
        print(f"Error: {exc}")
    finally:
        print("Deleting a student completed.\n")

#The main menu and handling user input
def main():
    """Run the student management menu."""
    initialize_files()
    while True:
        display_menu()
        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_student()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("Thank you for using the system.")
            logging.info("User exited the student management system.")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")
            logging.warning("Invalid menu choice entered: %s", choice)


if __name__ == "__main__":
    main()
