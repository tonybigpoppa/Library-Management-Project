from abc import ABC, abstractmethod
# ================================================================
# 1. ABSTRACT BASE CLASS + INHERITANCE HIERARCHY
# ================================================================
class LibraryItem(ABC):
    """Abstract base class for all items in the library."""

    def __init__(self, title, author):
        self.title = title
        self.author = author

    @abstractmethod
    def calculate_loan_period(self):
        """Each item sets its own loan period."""
        pass

    def description(self):
        """Common method for all items."""
        return f"'{self.title}' by {self.author}"


class Book(LibraryItem):
    """A standard library book."""

    def __init__(self, title, author, pages):
        super().__init__(title, author)
        self.pages = pages

    def calculate_loan_period(self):
        # Standard books get 14 days + page-based bonus
        base_period = 14
        if self.pages > 400:
            return base_period + 7  # long books get extra time
        return base_period

    def description(self):
        return f"Book: {super().description()} ({self.pages} pages)"


class Magazine(LibraryItem):
    """A magazine has a shorter loan period."""

    def __init__(self, title, author, issue_number):
        super().__init__(title, author)
        self.issue_number = issue_number

    def calculate_loan_period(self):
        # Magazines are short-term loans
        return 7

    def description(self):
        return f"Magazine: {super().description()} (Issue #{self.issue_number})"


class DVD(LibraryItem):
    """DVDs have special rules based on runtime."""

    def __init__(self, title, author, runtime_minutes):
        super().__init__(title, author)
        self.runtime_minutes = runtime_minutes

    def calculate_loan_period(self):
        # Longer DVDs get extra day
        base_period = 3
        if self.runtime_minutes > 120:
            return base_period + 1
        return base_period

    def description(self):
        return f"DVD: {super().description()} ({self.runtime_minutes} mins)"


# ================================================================
# 2. POLYMORPHISM DEMONSTRATION
# ================================================================
def print_loan_periods(items):
    """
    Demonstrates polymorphism:
    - Treats all objects as LibraryItem (base class reference)
    - Calls overridden methods depending on the subclass
    """
    for item in items:
        print(f"{item.description()} → Loan period: {item.calculate_loan_period()} days")


# ================================================================
# 3. COMPOSITION (has-a relationship)
# ================================================================
class Library:
    """
    Demonstrates composition:
    A Library *has* items, but is not a kind of LibraryItem.
    This is why composition is used instead of inheritance.
    """

    def __init__(self):
        self.items = []  # contains Book, Magazine, DVD instances

    def add_item(self, item: LibraryItem):
        self.items.append(item)

    def list_items(self):
        for item in self.items:
            print(item.description())


# ================================================================
# Example Usage 
# ================================================================
if __name__ == "__main__":
    # Create items
    b1 = Book("1984", "George Orwell", pages=328)
    b2 = Book("The Stand", "Stephen King", pages=823)
    m1 = Magazine("National Geographic", "Various", issue_number=202)
    d1 = DVD("Inception", "Christopher Nolan", runtime_minutes=148)

    # Polymorphism demo
    print("=== POLYMORPHISM DEMO ===")
    print_loan_periods([b1, b2, m1, d1])

    # Composition demo
    print("\n=== COMPOSITION DEMO (Library has items) ===")
    library = Library()
    library.add_item(b1)
    library.add_item(m1)
    library.add_item(d1)
    library.list_items()