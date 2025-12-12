# Project 4
# Library Management
# Team: Anthony Palma, Hanan Wolde, Darian La, Prince Olubuse-Omisore, Seena Rad
# main.py
"""
Simple Library Management System .
Provides:
- Book / Patron / Loan classes
- LibraryApp controller with persistence (JSON), CSV import/export
- CLI demo when run directly
Uses pathlib, context managers, and explicit error handling.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import uuid
import json
import csv

# ---------------------------
# Domain models
# ---------------------------

@dataclass
class Book:
    id: str
    title: str
    author: str
    year: Optional[int]
    copies_total: int
    copies_available: int

    @staticmethod
    def create(title: str, author: str, year: Optional[int], copies: int = 1) -> "Book":
        return Book(
            id=str(uuid.uuid4()),
            title=title,
            author=author,
            year=year,
            copies_total=copies,
            copies_available=copies,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        return cls(**data)


@dataclass
class Patron:
    id: str
    name: str
    email: str

    @staticmethod
    def create(name: str, email: str) -> "Patron":
        return Patron(id=str(uuid.uuid4()), name=name, email=email)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Patron":
        return cls(**data)


@dataclass
class Loan:
    id: str
    book_id: str
    patron_id: str
    loan_date: str
    return_date: Optional[str]

    @staticmethod
    def create(book_id: str, patron_id: str) -> "Loan":
        return Loan(
            id=str(uuid.uuid4()),
            book_id=book_id,
            patron_id=patron_id,
            loan_date=datetime.utcnow().isoformat(),
            return_date=None,
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Loan":
        return cls(**data)


# ---------------------------
# Persistence & I/O
# ---------------------------

class PersistenceError(Exception):
    pass


class LibraryApp:
    """
    Controller for library functions and persistence.
    """

    def __init__(self, state_path: Optional[Path] = None):
        base = Path(__file__).parent
        self.state_path: Path = (Path(state_path) if state_path else base / "library_state.json")
        self.books: Dict[str, Book] = {}
        self.patrons: Dict[str, Patron] = {}
        self.loans: Dict[str, Loan] = {}
        self._load_state_if_exists()

    # ------- Persistence (JSON) --------
    def save_state(self, path: Optional[Path] = None) -> None:
        path = Path(path) if path else self.state_path
        data = {
            "books": {bid: b.to_dict() for bid, b in self.books.items()},
            "patrons": {pid: p.to_dict() for pid, p in self.patrons.items()},
            "loans": {lid: l.to_dict() for lid, l in self.loans.items()},
        }
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise PersistenceError(f"Failed to save state to {path}: {e}")

    def _load_state_if_exists(self) -> None:
        if not self.state_path.exists():
            return
        try:
            with self.state_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = {bid: Book.from_dict(d) for bid, d in data.get("books", {}).items()}
            self.patrons = {pid: Patron.from_dict(d) for pid, d in data.get("patrons", {}).items()}
            self.loans = {lid: Loan.from_dict(d) for lid, d in data.get("loans", {}).items()}
        except Exception as e:
            raise PersistenceError(f"Failed to load state from {self.state_path}: {e}")

    def load_state(self, path: Path) -> None:
        p = Path(path)
        if not p.exists():
            raise PersistenceError(f"State file does not exist: {p}")
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            self.books = {bid: Book.from_dict(d) for bid, d in data.get("books", {}).items()}
            self.patrons = {pid: Patron.from_dict(d) for pid, d in data.get("patrons", {}).items()}
            self.loans = {lid: Loan.from_dict(d) for lid, d in data.get("loans", {}).items()}
            self.state_path = p
        except Exception as e:
            raise PersistenceError(f"Failed to load state: {e}")

    # ------- CSV import/export --------
    def import_books_from_csv(self, csv_path: Path) -> List[Book]:
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise PersistenceError(f"CSV file not found: {csv_path}")
        added = []
        try:
            with csv_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = (row.get("title") or row.get("Title") or "").strip()
                    author = (row.get("author") or row.get("Author") or "Unknown").strip()
                    year_raw = (row.get("year") or row.get("Year") or "").strip()
                    copies_raw = (row.get("copies") or row.get("Copies") or "1").strip()
                    year = int(year_raw) if year_raw.isdigit() else None
                    try:
                        copies = max(1, int(copies_raw))
                    except Exception:
                        copies = 1
                    if not title:
                        # skip invalid rows
                        continue
                    book = Book.create(title=title, author=author, year=year, copies=copies)
                    self.books[book.id] = book
                    added.append(book)
            return added
        except PersistenceError:
            raise
        except Exception as e:
            raise PersistenceError(f"Failed to import CSV {csv_path}: {e}")

    def export_books_to_csv(self, csv_path: Path) -> None:
        csv_path = Path(csv_path)
        try:
            # ensure parent exists
            csv_path.parent.mkdir(parents=True, exist_ok=True)
            with csv_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "title", "author", "year", "copies_total", "copies_available"])
                for b in self.books.values():
                    writer.writerow([b.id, b.title, b.author, b.year, b.copies_total, b.copies_available])
        except Exception as e:
            raise PersistenceError(f"Failed to export CSV to {csv_path}: {e}")

    # ------- Business logic --------
    def add_book(self, title: str, author: str, year: Optional[int], copies: int = 1) -> Book:
        book = Book.create(title=title, author=author, year=year, copies=copies)
        self.books[book.id] = book
        return book

    def add_patron(self, name: str, email: str) -> Patron:
        patron = Patron.create(name=name, email=email)
        self.patrons[patron.id] = patron
        return patron

    def checkout_book(self, book_id: str, patron_id: str) -> Loan:
        if book_id not in self.books:
            raise ValueError("Book not found")
        if patron_id not in self.patrons:
            raise ValueError("Patron not found")
        book = self.books[book_id]
        if book.copies_available < 1:
            raise ValueError("No copies available")
        book.copies_available -= 1
        loan = Loan.create(book_id=book_id, patron_id=patron_id)
        self.loans[loan.id] = loan
        return loan

    def return_book(self, loan_id: str) -> Loan:
        if loan_id not in self.loans:
            raise ValueError("Loan not found")
        loan = self.loans[loan_id]
        if loan.return_date is not None:
            raise ValueError("Book already returned")
        book = self.books.get(loan.book_id)
        if book:
            book.copies_available += 1
        loan.return_date = datetime.utcnow().isoformat()
        return loan

    # convenience: simple report
    def summary(self) -> dict:
        return {
            "books_total": len(self.books),
            "patrons_total": len(self.patrons),
            "loans_total": len(self.loans),
        }


# ---------------------------
# CLI demo (keeps file self-contained)
# ---------------------------
def demo_cli():
    import sys
    base = Path(__file__).parent
    app = LibraryApp()
    print("Simple Library Management (demo). State stored at:", app.state_path)
    while True:
        print("\n Menu (Enter only corresponding number with task): ")
        print("1) Add book")
        print("2) Add patron")
        print("3) Checkout book")
        print("4) Return book")
        print("5) Import books from CSV (enter path)")
        print("6) Export books to CSV (enter path)")
        print("7) Save state")
        print("8) Show summary")
        print("9) Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "1":
                title = input("Title: ").strip()
                author = input("Author: ").strip()
                year_raw = input("Year (leave blank if unknown): ").strip()
                copies_raw = input("Copies (default 1): ").strip() or "1"
                year = int(year_raw) if year_raw.isdigit() else None
                copies = int(copies_raw) if copies_raw.isdigit() else 1
                b = app.add_book(title, author, year, copies)
                print(f"Added book: {b.title} id={b.id}")
            elif choice == "2":
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                p = app.add_patron(name, email)
                print(f"Added patron: {p.name} id={p.id}")
            elif choice == "3":
                book_id = input("Book id: ").strip()
                patron_id = input("Patron id: ").strip()
                loan = app.checkout_book(book_id, patron_id)
                print(f"Checked out loan id: {loan.id}")
            elif choice == "4":
                loan_id = input("Loan id: ").strip()
                loan = app.return_book(loan_id)
                print(f"Returned loan id: {loan.id}")
            elif choice == "5":
                path = Path(input("CSV path (relative or absolute): ").strip())
                added = app.import_books_from_csv(path)
                print(f"Imported {len(added)} books.")
            elif choice == "6":
                out = Path(input("Export CSV path (relative or absolute): ").strip())
                app.export_books_to_csv(out)
                print(f"Exported to {out}")
            elif choice == "7":
                app.save_state()
                print(f"Saved to {app.state_path}")
            elif choice == "8":
                print(json.dumps(app.summary(), indent=2))
                # show first 5 books
                for b in list(app.books.values())[:5]:
                    print(f"- {b.title} ({b.copies_available}/{b.copies_total}) id={b.id}")
            elif choice == "9":
                app.save_state()
                print("Saved and exiting.")
                sys.exit(0)
            else:
                print("Invalid choice")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    demo_cli()