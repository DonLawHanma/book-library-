# Personal Book Library

INFO-1298 Project 2. A command-line app that manages a personal book library in a Python dictionary, loads records from `books.csv`, validates the data, and saves on exit.

## Features
- Add a book, update an author or year, delete a book (with confirmation)
- Search by title and display all books sorted by title
- CSV validation on load: bad rows are skipped with a warning
- Custom exceptions for invalid menu options, years and ISBNs

## Run
    python book_library.py

Requires Python 3.8 or newer. No external dependencies.

## CSV format
Header: `Title,Author,Year,ISBN`. Year must be 1000 up to the current year. ISBN must be digits only and at least 10 digits long.

Author: Ueza Congo
