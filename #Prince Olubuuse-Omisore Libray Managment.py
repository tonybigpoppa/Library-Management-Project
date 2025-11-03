#Prince Olubuuse-Omisore
books = [
    {"title": "The Pragmatic Programmer", "available": True, "user": None},
    {"title": "Clean Code", "available": True, "user": None},
    {"title": "Python Crash Course", "available": False, "user": "Anthony"},
    {"title": "Automate the Boring Stuff", "available": True, "user": None},
    {"title": "Introduction to Algorithms", "available": False, "user": "Sarah"}
]

users = [
    {"name": "Anthony", "borrowed_books": ["Python Crash Course"]},
    {"name": "Sarah", "borrowed_books": ["Introduction to Algorithms"]},
    {"name": "Prince", "borrowed_books": []},
    {"name": "Jamal", "borrowed_books": []} 
]



# Function 1 Assigning book to user 
def assign_book_to_user(book_title, user_name, books, users):
    """""
    Assigns a book to a user if it is available in the library.

    book_title = title of the book to be assigned
    user_name = name of the user borrowing the book
    books = list of dictionaries containing book information
    users = list of dictionaries containing user information
    """

    if not isinstance(book_title, str) or not isinstance(user_name, str):
        raise TypeError("Book title and user name must be strings.")

    # Search for the book
    book_found = None
    for book in books:
        if book["title"].lower() == book_title.lower():
            book_found = book
            break

    if not book_found:
        raise ValueError(f"Book '{book_title}' not found in library.")

    # Check availability
    if not book_found["available"]:
        print(f"Sorry, '{book_title}' is currently checked out by {book_found['user']}.")
        return False

    # Find user
    user_found = None
    for user in users:
        if user["name"].lower() == user_name.lower():
            user_found = user
            break

    if not user_found:
        raise ValueError(f"User '{user_name}' not found in system.")

    # Assigning book to user
    book_found["available"] = False
    book_found["user"] = user_found["name"]
    user_found["borrowed_books"].append(book_found["title"])

    print(f"Book '{book_found['title']}' assigned to user '{user_found['name']}' successfully.")
    return True


"""Testing"""
title_input = input("Enter the title of the book to assign: ")
user_input = input("Enter the user borrowing the book: ")
assign_book_to_user(title_input, user_input, books, users)





# Function 2 Check book availability
def check_book_availability(book_title, books):
    """
    Checks if a given book is available for borrowing.
    """

    if not isinstance(book_title, str):
        raise TypeError("Book title must be a string.")

    for book in books:
        if book["title"].lower() == book_title.lower():
            if book["available"]:
                print(f"'{book['title']}' is available for borrowing.")
                return True
            else:
                print(f"'{book['title']}' is currently checked out by {book['user']}.")
                return False

    raise ValueError(f"Book '{book_title}' not found in library.")


""" Testing"""
title_check = input("Enter a book title to check availability: ")
check_book_availability(title_check, books)






#Function 3 Checking book format 
def format_book_name(title):
    """
    Formats a book title consistently.
    - Removes extra spaces
    - Converts to Title Case
    - Handles edge cases (empty strings or non-string input)
    """

    if not isinstance(title, str):
        raise TypeError("Title must be a string.")

    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Title cannot be empty.")

    # Replacing multiple spaces with a single space
    while "  " in clean_title:
        clean_title = clean_title.replace("  ", " ")

    formatted_title = clean_title.title()

    print(f"Formatted title: '{formatted_title}'")
    return formatted_title


""" Testing """
title_to_format = input("Enter a book title to format: ")
format_book_name(title_to_format)

# add members
for u in users_data:
    catalog.register_member(Member(u["name"]))

# add books (preserve available and user fields)
for i, b in enumerate(books_data):
    bk = Book(item_id=str(i+1), title=b["title"], author="", isbn="")
    if not b["available"] and b["user"]:
        # mark as checked out to that user
        bk._available = False  # keep internal state consistent with original data
        bk._user = b["user"]
    catalog.add_book(bk)

print("Available books:", catalog.list_available_books())
print("Anthony borrowed:", catalog.list_member_books("Anthony"))

# Try checkout (should raise if unavailable)
try:
    loan = catalog.checkout("Clean Code", "Prince")
    print("Loan created:", loan)
except Exception as e:
    print("Checkout error:", e)

# Return a book
catalog.return_book("Python Crash Course", "Anthony")
print("After return, Anthony borrowed:", catalog.list_member_books("Anthony"))
print("Available books now:", catalog.list_available_books())

# Save state to a JSON file
catalog.save_to_file("/mnt/data/INST326_Project2_Catalog.json")
print("Saved catalog to /mnt/data/INST326_Project2_Catalog.json")

from __future__ import annotations
from datetime import datetime, timedelta
import json
from typing import List, Optional

class LibraryItem:
    """Represents a generic library item."""
    def __init__(self, item_id: str, title: str, item_type: str = "book", loan_period: int = 14):
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("item_id must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if loan_period < 0:
            raise ValueError("loan_period must be non-negative")
        self._item_id = item_id
        self._title = title.strip()
        self._item_type = item_type
        self._loan_period = int(loan_period)
        self._available = True

    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def item_type(self) -> str:
        return self._item_type

    @property
    def available(self) -> bool:
        return self._available

    def checkout(self) -> datetime:
        if not self._available:
            raise RuntimeError("Item not available for checkout")
        self._available = False
        return datetime.now() + timedelta(days=self._loan_period)

    def checkin(self) -> None:
        self._available = True

    def __str__(self):
        status = "Available" if self._available else "Checked out"
        return f"{self._title} ({self._item_type}) - {status}"

    def __repr__(self):
        return f"LibraryItem({self._item_id!r}, {self._title!r}, {self._item_type!r})"

class Book(LibraryItem):
    """Concrete Book keeping the same 'available' and single 'user' semantics (Option A)."""
    def __init__(self, item_id: str, title: str, author: str = "", isbn: str = "", loan_period: int = 14):
        super().__init__(item_id=item_id, title=title, item_type="book", loan_period=loan_period)
        self._author = author
        self._isbn = isbn
        self._user: Optional[str] = None  # name of user who checked out (Option A)

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def user(self) -> Optional[str]:
        return self._user

    def assign_to_user(self, user_name: str) -> datetime:
        if not self.available:
            raise RuntimeError("Book not available")
        if not isinstance(user_name, str) or not user_name.strip():
            raise ValueError("user_name must be a non-empty string")
        due = self.checkout()
        self._user = user_name
        return due

    def return_from_user(self) -> None:
        self.checkin()
        self._user = None

    def __repr__(self):
        return f"Book({self.item_id!r}, {self.title!r}, author={self._author!r})"

class Member:
    """Represents a library member."""
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        self._name = name.strip()
        self._borrowed: List[str] = []  # list of book titles (Option A)

    @property
    def name(self) -> str:
        return self._name

    @property
    def borrowed_books(self) -> List[str]:
        return list(self._borrowed)

    def borrow(self, book: Book) -> datetime:
        due = book.assign_to_user(self._name)
        self._borrowed.append(book.title)
        return due

    def return_book(self, book: Book) -> None:
        if book.title in self._borrowed:
            self._borrowed.remove(book.title)
        book.return_from_user()

    def __repr__(self):
        return f"Member({self._name!r})"

class Loan:
    """Represents a loan (ties a Book to a Member with a due date)."""
    def __init__(self, book: Book, member: Member, due_date: datetime):
        if not isinstance(book, Book):
            raise ValueError("book must be a Book")
        if not isinstance(member, Member):
            raise ValueError("member must be a Member")
        if not isinstance(due_date, datetime):
            raise ValueError("due_date must be a datetime")
        self._book = book
        self._member = member
        self._due_date = due_date

    @property
    def book(self) -> Book:
        return self._book

    @property
    def member(self) -> Member:
        return self._member


