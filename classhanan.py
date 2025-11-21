# Hanan Wolde
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


# ============================
# PROJECT 3 – ABSTRACT BASE CLASS
# ============================

class AbstractItem(ABC):
    """Abstract base class for all library items."""

    @abstractmethod
    def calculate_loan_period(self):
        """Polymorphic loan period implemented by subclasses."""
        pass


# ============================
# PROJECT 3 – BASE CLASS
# ============================

class LibraryItem(AbstractItem):
    """Base class for all items in the library."""

    def __init__(self, item_id, title):
        if not isinstance(item_id, str) or not isinstance(title, str):
            raise TypeError("Item ID and title must be strings.")
        if not item_id.strip() or not title.strip():
            raise ValueError("Item ID and title cannot be empty.")

        self._item_id = item_id
        self._title = title

    @property
    def item_id(self):
        return self._item_id

    @property
    def title(self):
        return self._title

    def __str__(self):
        return f"{self._title} (ID: {self._item_id})"

    def __repr__(self):
        return f"LibraryItem({self._item_id!r}, {self._title!r})"


# ============================
# PROJECT 3 – SUBCLASSES (INHERITANCE + POLYMORPHISM)
# ============================

class Book(LibraryItem):
    """Represents a book in the library."""

    def __init__(self, book_id, title, author):
        super().__init__(book_id, title)
        if not isinstance(author, str):
            raise TypeError("Author must be a string.")
        if not author.strip():
            raise ValueError("Author cannot be empty.")

        self._author = author
        self._is_reserved = False

    @property
    def author(self):
        return self._author

    @property
    def is_reserved(self):
        return self._is_reserved

    def reserve(self):
        if self._is_reserved:
            raise RuntimeError(f"Book '{self._title}' is already reserved.")
        self._is_reserved = True

    def cancel_reservation(self):
        self._is_reserved = False

    # Polymorphic loan period
    def calculate_loan_period(self):
        return 21  # 21 days for books

    def __str__(self):
        status = "Reserved" if self._is_reserved else "Available"
        return f"{self._title} by {self._author} ({status})"

    def __repr__(self):
        return f"Book({self._item_id!r}, {self._title!r}, {self._author!r})"


class Magazine(LibraryItem):
    """Magazine subclass with different loan period."""

    def calculate_loan_period(self):
        return 7  # 7-day loan period


class ResearchPaper(LibraryItem):
    """Research paper subclass with shortest loan period."""

    def calculate_loan_period(self):
        return 1  # 1-day loan period


# ============================
# PROJECT 2 – MEMBER CLASS
# ============================

class Member:
    """Represents a library member who can reserve books."""

    def __init__(self, member_id, name):
        if not member_id.strip() or not name.strip():
            raise ValueError("Member ID and name cannot be empty.")

        self._member_id = member_id
        self._name = name

    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name

    def __str__(self):
        return f"Member: {self._name} (ID: {self._member_id})"

    def __repr__(self):
        return f"Member({self._member_id!r}, {self._name!r})"


# ============================
# PROJECT 2 – RESERVATION
# ============================

class Reservation:
    """Handles the reservation of books by members."""

    def __init__(self, member, book, days=7):
        if not isinstance(member, Member) or not isinstance(book, Book):
            raise TypeError("Reservation requires a Member and a Book.")

        if book.is_reserved:
            raise RuntimeError(f"Book '{book.title}' is already reserved.")

        self._member = member
        self._book = book
        self._reserved_on = datetime.now()
        self._due_date = self._reserved_on + timedelta(days=days)
        book.reserve()

    @property
    def due_date(self):
        return self._due_date.strftime("%Y-%m-%d")

    def cancel(self):
        self._book.cancel_reservation()

    def __str__(self):
        return f"{self._book.title} reserved by {self._member.name} until {self.due_date}"

    def __repr__(self):
        return f"Reservation({self._member!r}, {self._book!r})"


# ============================
# PROJECT 3 – COMPOSITION IN LIBRARY
# ============================

class Library:
    """Main library system managing books and reservations."""

    def __init__(self):
        self._items = []          # composition: library HAS items
        self._reservations = []   # library HAS reservations

    def add_item(self, item):
        if not isinstance(item, LibraryItem):
            raise TypeError("Only LibraryItem objects can be added.")
        self._items.append(item)

    def reserve_book(self, member, book_id):
        for item in self._items:
            if isinstance(item, Book) and item.item_id == book_id:
                reservation = Reservation(member, item)
                self._reservations.append(reservation)
                return reservation
        raise ValueError("Book not found.")

    def check_status(self, book_id):
        for item in self._items:
            if isinstance(item, Book) and item.item_id == book_id:
                status = "Reserved" if item.is_reserved else "Available"
                return f"Book '{item.title}' is currently {status}."
        return "Book not found."

    def __str__(self):
        return f"Library with {len(self._items)} items and {len(self._reservations)} reservations."


# ============================
# PROJECT 2 — QR GENERATOR
# ============================

class QRCode:
    """Generates a simple text-based QR code for books."""

    @staticmethod
    def generate(book):
        if not isinstance(book, Book):
            raise TypeError("QR Code can only be generated for a Book object.")
        return (
            f"========== BOOK QR ==========\n"
            f"Book ID : {book.item_id}\n"
            f"Title   : {book.title}\n"
            f"Author  : {book.author}\n"
            f"============================="
        )


# ============================
# Example usage
# ============================

if __name__ == "__main__":
    library = Library()
    book1 = Book("B001", "The Great Gatsby", "F. Scott Fitzgerald")
    mag1 = Magazine("M101", "Tech Weekly")
    paper1 = ResearchPaper("R900", "Quantum Computing Notes")

    member1 = Member("M001", "Hanan")

    library.add_item(book1)
    library.add_item(mag1)
    library.add_item(paper1)

    print(library.reserve_book(member1, "B001"))
    print(library.check_status("B001"))
    print(QRCode.generate(book1))
