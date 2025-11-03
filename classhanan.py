# Hanan Wolde
from datetime import datetime, timedelta

# Represents a book in the library
class Book:

    def __init__(self, book_id, title, author):
        if not all(isinstance(x, str) for x in [book_id, title, author]):
            raise TypeError("Book ID, title, and author must be strings.")
        if not book_id.strip() or not title.strip() or not author.strip():
            raise ValueError("Book ID, title, and author cannot be empty.")

        self._book_id = book_id
        self._title = title
        self._author = author
        self._is_reserved = False

    @property
    def book_id(self):
        return self._book_id

    @property
    def title(self):
        return self._title

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

    def __str__(self):
        status = "Reserved" if self._is_reserved else "Available"
        return f"{self._title} by {self._author} ({status})"

    def __repr__(self):
        return f"Book({self._book_id!r}, {self._title!r}, {self._author!r})"


# Represents a library member who can reserve books
class Member:
    
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

# Handles the reservation of books by members
class Reservation:
    
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

# Main library system managing books and reservations
class Library:
    
    def __init__(self):
        self._books = []
        self._reservations = []

    def add_book(self, book):
        if not isinstance(book, Book):
            raise TypeError("Only Book objects can be added.")
        self._books.append(book)

    def reserve_book(self, member, book_id):
        for book in self._books:
            if book.book_id == book_id:
                reservation = Reservation(member, book)
                self._reservations.append(reservation)
                return reservation
        raise ValueError("Book not found.")

    def check_status(self, book_id):
        for book in self._books:
            if book.book_id == book_id:
                status = "Reserved" if book.is_reserved else "Available"
                return f"Book '{book.title}' is currently {status}."
        return "Book not found."

    def __str__(self):
        return f"Library with {len(self._books)} books and {len(self._reservations)} reservations."
 
# Generates a simple text-based QR code for books
class QRCode:
    
    @staticmethod
    def generate(book):
        if not isinstance(book, Book):
            raise TypeError("QR Code can only be generated for a Book object.")
        return (
            f"========== BOOK QR ==========\n"
            f"Book ID : {book.book_id}\n"
            f"Title   : {book.title}\n"
            f"Author  : {book.author}\n"
            f"============================="
        )

