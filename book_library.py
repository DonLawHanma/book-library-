"""
INFO-1298 Project 2 - Personal Book Library
Author: Ueza Congo
Purpose: Manage a personal book library using a Python dictionary,
load records from books.csv, validate data, and save on exit.


References:
- Python csv module documentation: https://docs.python.org/3/library/csv.html
- Python exceptions tutorial: https://docs.python.org/3/tutorial/errors.html
"""


import csv
from datetime import date


CURRENT_YEAR = date.today().year
BOOKS_FILE = "books.csv"


class InvalidMenuOptionError(Exception):
    pass


class InvalidYearError(Exception):
    pass


class InvalidISBNError(Exception):
    pass


def is_number(text):
    return text.isdigit()


def display_menu():
    print("\n------ Personal Book Library ------")
    print("1. Add a book")
    print("2. Update a book's author")
    print("3. Update a book's publication year")
    print("4. Search for a book by title")
    print("5. Delete a book")
    print("6. Display all books sorted by title")
    print("7. Save and Exit")
    print("-----------------------------------")


def load_books(filename):
    library = {}
    try:
        with open(filename, "r", newline="", encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            required_fields = ["Title", "Author", "Year", "ISBN"]

            if reader.fieldnames is None:
                raise ValueError("The CSV file is empty or missing a header row.")

            for field in required_fields:
                if field not in reader.fieldnames:
                    raise ValueError(f"Missing required CSV header: {field}")

            for line_number, row in enumerate(reader, start=2):
                try:
                    title = row.get("Title", "").strip()
                    author = row.get("Author", "").strip()
                    year_text = row.get("Year", "").strip()
                    isbn = row.get("ISBN", "").strip()

                    if not title or not author or not year_text or not isbn:
                        raise ValueError("Missing field")
                    if not year_text.isdigit():
                        raise ValueError("Year must be numeric")

                    year = int(year_text)
                    if not 1000 <= year <= CURRENT_YEAR:
                        raise ValueError("Year out of range")
                    if not isbn.isdigit() or len(isbn) < 10:
                        raise ValueError("ISBN must be numeric and at least 10 digits")

                    library[title] = {"author": author, "year": year, "isbn": isbn}
                except ValueError as err:
                    print(f"Warning: Skipping invalid record on line {line_number}: {err}")
    except FileNotFoundError:
        print("Error: The specified file was not found. A new file will be created when you save and exit.")
    except PermissionError:
        print("Error: Permission denied when accessing the file.")
    except Exception as err:
        print(f"An unexpected error occurred while loading the file: {err}")

    return library


def save_books(filename, library):
    try:
        with open(filename, "w", newline="", encoding="utf-8") as outfile:
            fieldnames = ["Title", "Author", "Year", "ISBN"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for title in sorted(library):
                book = library[title]
                writer.writerow({
                    "Title": title,
                    "Author": book["author"],
                    "Year": book["year"],
                    "ISBN": book["isbn"],
                })
        print(f"Library saved to {filename}.")
        return True
    except PermissionError:
        print("Error: Permission denied when saving the file.")
    except OSError as err:
        print(f"Error: The file could not be saved: {err}")
    except Exception as err:
        print(f"An unexpected error occurred while saving the file: {err}")
    return False


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be blank.")


def get_valid_year(prompt):
    while True:
        year_input = input(prompt).strip()
        try:
            if not is_number(year_input):
                raise InvalidYearError("Year must be numeric.")
            year = int(year_input)
            if not 1000 <= year <= CURRENT_YEAR:
                raise InvalidYearError(f"Year must be between 1000 and {CURRENT_YEAR}.")
            return year
        except InvalidYearError as err:
            print(err)


def get_valid_isbn(prompt):
    while True:
        isbn = input(prompt).strip()
        try:
            if not isbn.isdigit() or len(isbn) < 10:
                raise InvalidISBNError("ISBN must be numeric and at least 10 digits.")
            return isbn
        except InvalidISBNError as err:
            print(err)


def add_book(library):
    title = get_non_empty_input("Enter book title: ")
    while title in library:
        print("Title already exists.")
        title = get_non_empty_input("Enter book title: ")

    author = get_non_empty_input("Enter author: ")
    year = get_valid_year("Enter publication year: ")
    isbn = get_valid_isbn("Enter ISBN: ")

    library[title] = {"author": author, "year": year, "isbn": isbn}
    print("Book has been added.")


def update_author(library):
    title = input("Enter book title: ").strip()
    if title not in library:
        print("Book not found.")
        return

    new_author = get_non_empty_input("Enter new author: ")
    library[title]["author"] = new_author
    print("Author updated successfully.")


def update_year(library):
    title = input("Enter book title: ").strip()
    if title not in library:
        print("Book not found.")
        return

    year = get_valid_year("Enter new publication year: ")
    library[title]["year"] = year
    print("Year updated successfully.")


def search_book(library):
    title = input("Enter book title to search: ").strip()
    if title in library:
        book = library[title]
        print(f"Title: {title}")
        print(f"Author: {book['author']}")
        print(f"Year: {book['year']}")
        print(f"ISBN: {book['isbn']}")
    else:
        print("Book not found.")


def delete_book(library):
    title = input("Enter book title to delete: ").strip()
    if title not in library:
        print("Book not found.")
        return

    confirm = input("Are you sure? (Y/N): ").strip().upper()
    if confirm == "Y":
        del library[title]
        print("Book deleted.")
    else:
        print("Cancelled.")


def display_books(library):
    if not library:
        print("No books in the library.")
        return

    for title in sorted(library):
        book = library[title]
        print("-------------------------")
        print(f"Title: {title}")
        print(f"Author: {book['author']}")
        print(f"Year: {book['year']}")
        print(f"ISBN: {book['isbn']}")
    print("-------------------------")


def confirm_save_and_exit(library):
    while True:
        confirm = input("Do you want to save and exit? (Y/N): ").strip().upper()
        if confirm == "Y":
            return save_books(BOOKS_FILE, library)
        if confirm == "N":
            print("Exit cancelled.")
            return False
        print("Please enter Y or N.")


def get_menu_choice():
    choice_input = input("Select a menu option (1-7): ").strip()
    if not is_number(choice_input):
        raise InvalidMenuOptionError("Menu option must be numeric.")

    choice = int(choice_input)
    if choice < 1 or choice > 7:
        raise InvalidMenuOptionError("Pick only a number from 1 to 7.")
    return choice


def main():
    library = load_books(BOOKS_FILE)

    while True:
        display_menu()
        try:
            choice = get_menu_choice()

            if choice == 1:
                add_book(library)
            elif choice == 2:
                update_author(library)
            elif choice == 3:
                update_year(library)
            elif choice == 4:
                search_book(library)
            elif choice == 5:
                delete_book(library)
            elif choice == 6:
                display_books(library)
            elif choice == 7:
                if confirm_save_and_exit(library):
                    print("Goodbye!")
                    break
        except InvalidMenuOptionError as err:
            print(f"Error: {err}")


if __name__ == "__main__":
    main()
