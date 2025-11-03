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

""" Testing """
title_to_format = input("Enter a book title to format: ")
format_book_name(title_to_format)

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

    @property
    def due_date(self) -> datetime:
        return self._due_date

    def is_overdue(self) -> bool:
        return datetime.now() > self._due_date

    def days_overdue(self) -> int:
        if not self.is_overdue():
            return 0
        return (datetime.now() - self._due_date).days

    def __repr__(self):
        return f"Loan(book={self._book.title!r}, member={self._member.name!r}, due={self._due_date.date()!r})"

class Catalog:
    """Manages a collection of Book objects and Member records."""
    def __init__(self):
        self._books: List[Book] = []
        self._members: List[Member] = []
        self._loans: List[Loan] = []

    @property
    def books(self) -> List[Book]:
        return list(self._books)

    @property
    def members(self) -> List[Member]:
        return list(self._members)

    def add_book(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise ValueError("must add a Book instance")
        # keep original semantics: do not allow duplicate titles
        if any(b.title.lower() == book.title.lower() for b in self._books):
            raise ValueError("Book already exists in catalog")
        self._books.append(book)

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for b in self._books:
            if b.title.lower() == title.lower():
                return b
        return None

    def remove_book(self, title: str) -> bool:
        b = self.find_book_by_title(title)
        if b:
            if not b.available:
                raise RuntimeError("Cannot remove a checked-out book")
            self._books.remove(b)
            return True
        return False

    def register_member(self, member: Member) -> None:
        if not isinstance(member, Member):
            raise ValueError("member must be Member")
        if any(m.name.lower() == member.name.lower() for m in self._members):
            raise ValueError("Member already registered")
        self._members.append(member)

    def find_member(self, name: str) -> Optional[Member]:
        for m in self._members:
            if m.name.lower() == name.lower():
                return m
        return None

    def checkout(self, title: str, member_name: str) -> Loan:
        book = self.find_book_by_title(title)
        if not book:
            raise ValueError("Book not found")
        member = self.find_member(member_name)
        if not member:
            raise ValueError("Member not found")
        due = member.borrow(book)
        loan = Loan(book=book, member=member, due_date=due)
        self._loans.append(loan)
        return loan

    def return_book(self, title: str, member_name: str) -> bool:
        book = self.find_book_by_title(title)
        member = self.find_member(member_name)
        if not book or not member:
            raise ValueError("Book or member not found")
        member.return_book(book)
        
        self._loans = [l for l in self._loans if not (l.book.title==title and l.member.name==member_name)]
        return True

    def list_available_books(self) -> List[str]:
        return [b.title for b in self._books if b.available]

    def list_member_books(self, member_name: str) -> List[str]:
        m = self.find_member(member_name)
        if not m:
            raise ValueError("Member not found")
        return m.borrowed_books

    def serialize(self) -> dict:
        return {
            "books": [{ "title": b.title, "author": b.author, "isbn": b.isbn, "available": b.available, "user": b.user } for b in self._books],
            "members": [{ "name": m.name, "borrowed_books": m.borrowed_books } for m in self._members]
        }

    def save_to_file(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.serialize(), f, indent=2)
