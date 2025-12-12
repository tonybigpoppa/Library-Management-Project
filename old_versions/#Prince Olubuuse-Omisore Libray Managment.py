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

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import json
from typing import List, Optional


# -----------------------------
# ABSTRACT BASE CLASS (REQUIRED)
# -----------------------------
class AbstractLibraryItem(ABC):
    """Abstract base class enforcing required interface for library items."""

    @abstractmethod
    def calculate_loan_period(self) -> int:
        """Each subclass must implement its own loan period logic."""
        pass

    @abstractmethod
    def checkout(self) -> datetime:
        """Must be implemented by subclasses."""
        pass


# -----------------------------
# BASE CLASS
# -----------------------------
class LibraryItem(AbstractLibraryItem):
    """Base class for all library items."""

    def __init__(self, item_id: str, title: str, item_type: str):
        if not isinstance(item_id, str) or not item_id.strip():
            raise ValueError("item_id must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")

        self._item_id = item_id
        self._title = title.strip()
        self._item_type = item_type
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

    # Default loan period — overridden in subclasses
    def calculate_loan_period(self) -> int:
        return 14  # default 2 weeks

    def checkout(self) -> datetime:
        if not self._available:
            raise RuntimeError("Item not available")
        self._available = False
        days = self.calculate_loan_period()
        return datetime.now() + timedelta(days=days)

    def checkin(self) -> None:
        self._available = True

    def __str__(self):
        status = "Available" if self._available else "Checked out"
        return f"{self._title} ({self._item_type}) - {status}"


# -----------------------------
# SUBCLASS #1 — BOOK (POLYMORPHIC)
# -----------------------------
class Book(LibraryItem):
    """Book item: has author + ISBN. Loan period = 14 days."""

    def __init__(self, item_id: str, title: str, author: str = "", isbn: str = ""):
        super().__init__(item_id=item_id, title=title, item_type="book")
        self._author = author
        self._isbn = isbn
        self._user: Optional[str] = None

    @property
    def author(self):
        return self._author

    @property
    def isbn(self):
        return self._isbn

    def calculate_loan_period(self) -> int:
        return 14  # Books get 2 weeks

    def assign_to_user(self, user_name: str) -> datetime:
        due = self.checkout()
        self._user = user_name
        return due

    def return_from_user(self):
        self.checkin()
        self._user = None


# -----------------------------
# SUBCLASS #2 — JOURNAL (POLYMORPHIC)
# -----------------------------
class Journal(LibraryItem):
    """Journal item: shorter loan time."""

    def __init__(self, item_id: str, title: str, volume: int):
        super().__init__(item_id=item_id, title=title, item_type="journal")
        self._volume = volume

    def calculate_loan_period(self) -> int:
        return 7  # Journals = 1 week


# -----------------------------
# SUBCLASS #3 — DVD (POLYMORPHIC)
# -----------------------------
class DVD(LibraryItem):
    """DVD item: shortest loan time."""

    def __init__(self, item_id: str, title: str, runtime_minutes: int):
        super().__init__(item_id=item_id, title=title, item_type="dvd")
        self._runtime_minutes = runtime_minutes

    def calculate_loan_period(self) -> int:
        return 3  # DVDs = 3 days


# -----------------------------
# MEMBER
# -----------------------------
class Member:
    def __init__(self, name: str):
        self._name = name
        self._borrowed: List[str] = []

    @property
    def name(self) -> str:
        return self._name

    def borrow(self, item: LibraryItem) -> datetime:
        due = item.checkout()
        self._borrowed.append(item.title)
        return due

    def return_item(self, item: LibraryItem):
        if item.title in self._borrowed:
            self._borrowed.remove(item.title)
        item.checkin()


# -----------------------------
# LOAN — Composition
# -----------------------------
class Loan:
    """A Loan object composes a Member + LibraryItem."""

    def __init__(self, item: LibraryItem, member: Member, due_date: datetime):
        self._item = item
        self._member = member
        self._due_date = due_date

    @property
    def item(self):
        return self._item

    @property
    def member(self):
        return self._member

    @property
    def due_date(self):
        return self._due_date


# -----------------------------
# CATALOG — Composition of Items + Members + Loans
# -----------------------------
class Catalog:
    def __init__(self):
        self._items: List[LibraryItem] = []
        self._members: List[Member] = []
        self._loans: List[Loan] = []

    def add_item(self, item: LibraryItem):
        self._items.append(item)

    def register_member(self, member: Member):
        self._members.append(member)

    def find_member(self, name: str) -> Optional[Member]:
        return next((m for m in self._members if m.name.lower() == name.lower()), None)

    def find_item(self, title: str) -> Optional[LibraryItem]:
        return next((i for i in self._items if i.title.lower() == title.lower()), None)

    def checkout(self, title: str, member_name: str) -> Loan:
        item = self.find_item(title)
        member = self.find_member(member_name)

        if not item:
            raise ValueError("Item not found.")
        if not member:
            raise ValueError("Member not found.")

        due = member.borrow(item)
        loan = Loan(item, member, due)
        self._loans.append(loan)
        return loan

    def return_item(self, title: str, member_name: str):
        item = self.find_item(title)
        member = self.find_member(member_name)
        member.return_item(item)

        self._loans = [l for l in self._loans if l.item.title != title or l.member.name != member_name]

