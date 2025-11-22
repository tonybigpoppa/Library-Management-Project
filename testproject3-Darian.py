import unittest
from abc import ABC
from project3Darian import LibraryItem, Book, Magazine, DVD, Library

class TestInheritance(unittest.TestCase):
    """Tests that inherited and overridden methods work correctly."""

    def test_book_inherits_description(self):
        b = Book("Test Book", "Author A", 200)
        self.assertIn("Book:", b.description())

    def test_magazine_overrides_description(self):
        m = Magazine("Nature", "Various", 50)
        self.assertTrue("Magazine:" in m.description())

    def test_dvd_overrides_loan_period(self):
        d = DVD("Movie", "Director", 150)
        self.assertGreater(d.calculate_loan_period(), 3)


class TestPolymorphism(unittest.TestCase):
    """Ensures polymorphic behavior is correct."""

    def test_polymorphic_loan_periods(self):
        items = [
            Book("A", "B", 300),
            Magazine("C", "D", 5),
            DVD("E", "F", 200)
        ]

        # Polymorphic method call
        loan_periods = [item.calculate_loan_period() for item in items]

        self.assertEqual(loan_periods[0], 14)     # Book
        self.assertEqual(loan_periods[1], 7)      # Magazine
        self.assertEqual(loan_periods[2], 4)      # DVD (long runtime → 3 + 1)


class TestAbstractClass(unittest.TestCase):
    """Tests enforcing abstract class rules."""

    def test_cannot_instantiate_library_item(self):
        # Attempting to instantiate an abstract class should raise TypeError
        with self.assertRaises(TypeError):
            LibraryItem("Title", "Author")


class TestComposition(unittest.TestCase):
    """Tests that composition (Library has items) works."""

    def test_library_contains_items(self):
        lib = Library()
        book = Book("1984", "Orwell", 328)
        mag = Magazine("Time", "Various", 100)

        lib.add_item(book)
        lib.add_item(mag)

        self.assertEqual(len(lib.items), 2)
        self.assertIs(lib.items[0], book)
        self.assertIs(lib.items[1], mag)

    def test_composition_type(self):
        """Library should NOT be a subclass of LibraryItem."""
        self.assertFalse(issubclass(Library, LibraryItem))


if __name__ == "__main__":
    unittest.main()