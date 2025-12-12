# test_main.py
"""
Tests for main.py LibraryApp
Contains:
- Unit tests for models and small functions
- Integration tests for interactions & persistence
- System tests for end-to-end workflows (import -> checkout -> save -> load -> export)
Uses unittest and temporary files/dirs so no extra repo files are required.
"""

import unittest
import tempfile
from pathlib import Path
import json
import csv
import os

# import classes from main.py (assumes both files are in same folder)
from main import Book, Patron, Loan, LibraryApp, PersistenceError


class UnitTests(unittest.TestCase):
    def test_book_create_and_to_from_dict(self):
        b = Book.create("A Title", "An Author", 1991, copies=2)
        d = b.to_dict()
        self.assertEqual(d["title"], "A Title")
        b2 = Book.from_dict(d)
        self.assertEqual(b2.title, "A Title")
        self.assertEqual(b2.copies_total, 2)

    def test_patron_create(self):
        p = Patron.create("Alice", "alice@example.com")
        self.assertTrue(p.id)
        self.assertEqual(p.email, "alice@example.com")

    def test_loan_create_and_from_dict(self):
        l = Loan.create("bookid", "patronid")
        d = l.to_dict()
        self.assertEqual(d["book_id"], "bookid")
        l2 = Loan.from_dict(d)
        self.assertEqual(l2.book_id, "bookid")


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # create app with temp file for state to avoid interfering with local files
        self.tmpdir = tempfile.TemporaryDirectory()
        self.state_path = Path(self.tmpdir.name) / "state.json"
        self.app = LibraryApp(state_path=self.state_path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_add_book_and_patron_and_checkout_return(self):
        b = self.app.add_book("IntTest Book", "Auth", 2000, copies=1)
        p = self.app.add_patron("Bob", "bob@example.com")
        # checkout
        loan = self.app.checkout_book(b.id, p.id)
        self.assertEqual(self.app.books[b.id].copies_available, 0)
        # return
        ret = self.app.return_book(loan.id)
        self.assertIsNotNone(ret.return_date)
        self.assertEqual(self.app.books[b.id].copies_available, 1)

    def test_save_and_load_state(self):
        b = self.app.add_book("Persist Book", "Auth", 2010, copies=2)
        p = self.app.add_patron("Carol", "c@example.com")
        loan = self.app.checkout_book(b.id, p.id)
        # save
        self.app.save_state(self.state_path)
        # create new app and load
        app2 = LibraryApp(state_path=self.state_path)
        # app2 will auto load from provided state_path in its constructor
        self.assertIn(b.id, app2.books)
        self.assertIn(p.id, app2.patrons)
        self.assertTrue(len(app2.loans) >= 1)


class SystemTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmpdir_path = Path(self.tmpdir.name)
        self.state_path = self.tmpdir_path / "system_state.json"
        self.app = LibraryApp(state_path=self.state_path)
        # create a sample CSV for import
        self.sample_csv = self.tmpdir_path / "sample_books.csv"
        with self.sample_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "author", "year", "copies"])
            writer.writerow(["SCSV Book 1", "Auth One", "2001", "2"])
            writer.writerow(["SCSV Book 2", "Auth Two", "", "1"])
            writer.writerow([",", "Bad Row", "1999", "1"])  # title is "," (valid), still created

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_end_to_end_import_checkout_save_load_export(self):
        # import
        added = self.app.import_books_from_csv(self.sample_csv)
        self.assertGreaterEqual(len(added), 2)
        # create patron and checkout first book
        patron = self.app.add_patron("EndUser", "end@example.com")
        book = next(iter(self.app.books.values()))
        loan = self.app.checkout_book(book.id, patron.id)
        self.assertEqual(self.app.books[book.id].copies_available, book.copies_total - 1)
        # export books
        export_csv = self.tmpdir_path / "exported.csv"
        self.app.export_books_to_csv(export_csv)
        self.assertTrue(export_csv.exists())
        # save state
        self.app.save_state(self.state_path)
        self.assertTrue(self.state_path.exists())
        # load into new app
        app2 = LibraryApp(state_path=self.state_path)
        self.assertIn(book.id, app2.books)
        self.assertIn(patron.id, app2.patrons)
        # ensure loans persisted
        self.assertTrue(any(l.book_id == book.id for l in app2.loans.values()))

    def test_import_missing_file_raises(self):
        missing = self.tmpdir_path / "does_not_exist.csv"
        with self.assertRaises(PersistenceError):
            self.app.import_books_from_csv(missing)

# Run tests
if __name__ == "__main__":
    unittest.main()