from abc import ABC, abstractmethod
from typing import List

#-----------------------------------------------------------------#

# IMPORTANT MESSAGE: Going forward this is going to be the file where all my programming is done. I changed the name later to reflect that.
# HOWEVER!! Because this version does not contain the full edit history of the original (Anthonys-Functions.py), I will turn in this version alongside the original.
# Please only consider this version when grading. If there is any confusion please reach out to me.

#-----------------------------------------------------------------#

# Anthonys Functions
titles = [
    "The Pragmatic Programmer", "Clean Code", "Python Crash Course",
    "Automate the Boring Stuff", "Introduction to Algorithms"
]
authors = [
    "Andrew Hunt & David Thomas", "Robert C. Martin", "Eric Matthes",
    "Al Sweigart", "Cormen, Leiserson, Rivest, Stein"
]
isbn = [
    "1234567891234", "1234567891235", "1234567891236",
    "1234567891237", "1234567891238"
]
is_checked_out = [False, False, True, False, True]

days_over = input("How many days overdue is the users book?: ")

def overdue_fine(days_over: int, fine = 0.25, max_days = 14):
    """ 
    Calculates the fine for having a book overdue.
    
    fine = the daily fine for having an overdue book
    days_over = the amount of days overdue
    max_days = the max amount of days the fine will be calculated for

    """

    try:
        days_over = int(days_over)
    except:
        raise TypeError("Incorrect input.")

    if not isinstance(days_over, int):
        raise ValueError("Please re-run the script and enter a number.")
    
    if days_over < max_days:
        return f"This users fine is: ${days_over * fine}"
    elif days_over > 31:
        return f"This book is missing."
    else:
        return f"This user has hit the maximum fine of ${max_days * fine}"
    
""" Test case """
overdue_fine(days_over)

#-----------------------------------------------------------------#

# 2: Add book to library

new_title = input("Enter the new book title: ")
new_author = input("Enter the new books author: ")
new_isbn = input("Enter the new books isbn: ")


def add_book(new_title, new_author, new_isbn, titles, authors, isbn, is_checked_out):
    """
    Adds a new book to the library list of books.

    titles, authors, isbn, is_checked_out = these are all the lists that make up the current library of books
    new_title, new_author, new_isbn = the attributes of the new book being added

    """
    check1 = len(titles)
    check2 = len(authors)
    check3 = len(isbn)

    if not isinstance(new_title, str):
        raise ValueError("Please re-run the script and enter a string.")
    
    if not isinstance(new_author, str):
        raise ValueError("Please re-run the script and enter a string.")
    
    if not isinstance(new_isbn, str):
        raise ValueError("Please re-run the script and enter a string.")
    
    if len(new_isbn) != 13:
        raise ValueError("ISBN must be 13 charcters.")

    titles.append(new_title)
    authors.append(new_author)
    isbn.append(new_isbn)
    is_checked_out.append(False)

    if len(titles) > check1 and len(authors) > check2 and len(isbn) > check3:
        return f"New book successfully added"
    else:
        return f"New book not added."

""" Test case """
add_book(new_title, new_author, new_isbn, titles, authors, isbn, is_checked_out)

#-----------------------------------------------------------------#

# 3: Declare book missing

def missing(days_over = int, missing = 31):
    """
    Create the circumstances for declaring a book as missing. 
    This would be when the library sends notices to households
    associated with the missing book and considers finding 
    other ways of collecting the book.

    days_over = the same value as before

    missing = the threshold for declaring a book missing

    """
    try:
        days_over = int(days_over)
    except:
        raise TypeError("Incorrect input.")
    
    if days_over < 60:
        return f"Book has been missing for {days_over - missing} days. Consider setting a overdue letter to the checkee. {overdue_fine(days_over)}"
    elif 61 < days_over < 120:
        return f"Book has been missing for {days_over - missing} days. A second letter must be sent. {overdue_fine(days_over)}"
    elif days_over > 120:
        return f"Book has been missing for {days_over - missing} days. The book is now considered stolen and should be collected on or paid for. {overdue_fine(days_over)}"
    else:
        return f"Book not missing yet."
    
""" Test Case """
missing(days_over)

class LibraryPatron:
    """
    A class representing a library patron with borrowing privileges and fine tracking.
    
    Attributes:
        _name (str): The patron's name
        _patron_id (str): Unique identifier for the patron
        _books_checked_out (list): List of ISBNs currently checked out
        _total_fines (float): Total fines owed by the patron
        _overdue_function (callable): External function to calculate overdue fines
    """
    
    def __init__(self, name: str, patron_id: str, overdue_function):
        """
        Initialize a LibraryPatron instance.
        
        Args:
            name: The full name of the patron (must be non-empty string)
            patron_id: Unique identifier for the patron (must be non-empty string)
            overdue_function: External function to calculate overdue fines
            
        Raises:
            ValueError: If name or patron_id are empty strings
            TypeError: If name or patron_id are not strings
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(patron_id, str):
            raise TypeError("Patron ID must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        if not patron_id.strip():
            raise ValueError("Patron ID cannot be empty.")
        
        self._name = name.strip()
        self._patron_id = patron_id.strip()
        self._books_checked_out = []
        self._total_fines = 0.0
        self._overdue_function = overdue_function
    
    @property
    def name(self) -> str:
        """Get the patron's name."""
        return self._name
    
    @property
    def patron_id(self) -> str:
        """Get the patron's ID."""
        return self._patron_id
    
    @property
    def books_checked_out(self) -> list:
        """Get list of books currently checked out (read-only)."""
        return self._books_checked_out.copy()
    
    @property
    def total_fines(self) -> float:
        """Get the total fines owed by the patron."""
        return self._total_fines
    
    def check_out_book(self, isbn: str) -> str:
        """
        Check out a book for the patron.
        """
        if not isinstance(isbn, str):
            raise TypeError("ISBN must be a string.")
        if len(isbn) != 13:
            raise ValueError("ISBN must be 13 characters.")
        
        self._books_checked_out.append(isbn)
        return f"Book checked out successfully. Total books: {len(self._books_checked_out)}"
    
    def return_book(self, isbn: str) -> str:
        """
        Return a book that was checked out.
        """
        if isbn in self._books_checked_out:
            self._books_checked_out.remove(isbn)
            return f"Book returned successfully. Total books: {len(self._books_checked_out)}"
        else:
            return f"Book with ISBN {isbn} not found in checked out books."
    
    def add_fine(self, amount: float) -> None:
        """
        Add a fine to the patron's account.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Fine amount must be a number.")
        if amount <= 0:
            raise ValueError("Fine amount must be positive.")
        
        self._total_fines += amount
    
    def pay_fine(self, amount: float) -> str:
        """
        Pay towards the patron's fines.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Payment amount must be a number.")
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        if amount > self._total_fines:
            raise ValueError("Payment cannot exceed total fines.")
        
        self._total_fines -= amount
        return f"Payment of ${amount:.2f} accepted. Remaining balance: ${self._total_fines:.2f}"
    
    def calculate_overdue_fine(self, days_over: int) -> str:
        """
        Calculate overdue fine using the external overdue_fine function.
        """
        result = self._overdue_function(days_over)
        
        if "fine is: $" in result:
            fine_amount = float(result.split("$")[1])
            self.add_fine(fine_amount)
        elif "maximum fine of $" in result:
            fine_amount = float(result.split("$")[1])
            self.add_fine(fine_amount)
        
        return result
    
    def __str__(self) -> str:
        """
        Return informal string representation of the patron.
        """
        book_count = len(self._books_checked_out)
        return f"Patron: {self._name} (ID: {self._patron_id}) - Books: {book_count} - Fines: ${self._total_fines:.2f}"
    
    def __repr__(self) -> str:
        """
        Return formal string representation of the patron.
        """
        return f"LibraryPatron(name='{self._name}', patron_id='{self._patron_id}')"


def overdue_fine(days_over: int, fine=0.25, max_days=14):
    try:
        days_over = int(days_over)
    except:
        raise TypeError("Incorrect input.")

    if not isinstance(days_over, int):
        raise ValueError("Please re-run the script and enter a number.")
    
    if days_over < max_days:
        return f"This users fine is: ${days_over * fine}"
    elif days_over > 31:
        return f"This book is missing."
    else:
        return f"This user has hit the maximum fine of ${max_days * fine}"

class AbstractItem(ABC):
    """Abstract base class for all library items"""
    
    def __init__(self, title: str, item_id: str):
        self.title = title
        self.item_id = item_id
        self.is_checked_out = False
        self.checked_out_to = None

    @abstractmethod
    def calculate_loan_period(self) -> int:
        """Calculate the loan period in days"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Get detailed description of the item"""
        pass

    def check_out(self, patron_id: str) -> str:
        """Check out this item to a patron"""
        if self.is_checked_out:
            return f"{self.title} is already checked out"
        self.is_checked_out = True
        self.checked_out_to = patron_id
        return f"{self.title} checked out successfully"
    
    def return_item(self) -> str:
        """Return this item"""
        if not self.is_checked_out:
            return f"{self.title} is not checked out"
        self.is_checked_out = False
        self.checked_out_to = None
        return f"{self.title} returned successfully"
    
    def __str__(self):
        return f"{self.get_description()} - Loan: {self.calculate_loan_period()} days"
    
class Book(AbstractItem):
    """Book class with longest loan period"""

    def __init__(self, title: str, item_id: str, author: str, pages: int):
        super().__init__(title, item_id) 
        self.author = author
        self.pages = pages

    def calculate_loan_period(self) -> int:
        """Books have the longest loan period"""
        return 21 
    
    def get_description(self) -> str:
        return f"Book: {self.title} by {self.author} ({self.pages} pages)"    

class DVD(AbstractItem):
    """DVD class with shortest loan period"""
    
    def __init__(self, title: str, item_id: str, director: str, runtime: int):
        super().__init__(title, item_id) 
        self.director = director
        self.runtime = runtime    

    def calculate_loan_period(self) -> int:
        """DVDs have the shortest loan period"""
        return 7 

    def get_description(self) -> str:
        return f"DVD: {self.title} directed by {self.director} ({self.runtime} min)"

class Magazine(AbstractItem):
    """Magazine class with medium loan period"""

    def __init__(self, title: str, item_id: str, issue: str, publisher: str):
        super().__init__(title, item_id) 
        self.issue = issue
        self.publisher = publisher

    def calculate_loan_period(self) -> int:
        """Magazines have medium loan period"""
        return 14 

    def get_description(self) -> str:
        return f"Magazine: {self.title} - {self.issue} by {self.publisher}"

class Library:
    """
    Library class that uses COMPOSITION to contain library items
    Rationale: A Library has items, but isn't a type of item itself
    """

    def __init__(self):
        self._items: List[AbstractItem] = []  

    def add_item(self, item: AbstractItem) -> None:
        """Add an item to the library"""
        self._items.append(item)

    def find_item(self, item_id: str) -> AbstractItem:
        """Find an item by ID"""
        for item in self._items:
            if item.item_id == item_id:
                return item
        raise ValueError(f"Item with ID {item_id} not found")

    def get_all_items(self) -> List[AbstractItem]:
        """Get all items in the library"""
        return self._items.copy()

    def checkout_item(self, item_id: str, patron_id: str) -> str:
        """Check out an item from the library"""
        item = self.find_item(item_id)
        return item.check_out(patron_id)

def demonstrate_polymorphism():
    """Polymorphic behavior demonstration"""

    items = [
        Book("The Pragmatic Programmer", "B001", "Andrew Hunt & David Thomas", 352),
        DVD("Inception", "D001", "Christopher Nolan", 148),
        Magazine("Time", "M001", "January 2024", "Time USA")
    ]

    print("=== POLYMORPHISM DEMONSTRATION ===")
    print("Same method call -> Different behaviors:\n")

    for item in items:
        print(f"{item.calculate_loan_period()} days - {item.get_description()}")
    
    print(f"\nTotal items processed uniformly: {len(items)}")

class EnhancedLibraryPatron(LibraryPatron):
    """Enhanced patron class that works with the new item system"""

    def __init__(self, name: str, patron_id: str, overdue_function):
        super().__init__(name, patron_id, overdue_function)
        self._borrowed_items = []

    def borrow_item(self, item: AbstractItem) -> str:
        """Borrow an item using the new system"""
        result = item.check_out(self.patron_id)
        if "successfully" in result:
            self._borrowed_items.append(item)
        return result

    def return_borrowed_item(self, item_id: str) -> str:
        """Return a borrowed item"""
        for item in self._borrowed_items:
            if item.item_id == item_id:
                result = item.return_item()
                if "returned" in result:
                    self._borrowed_items.remove(item)
                return result
        return f"Item {item_id} not found in borrowed items"

# Test Case
patron = LibraryPatron("John Doe", "P123", overdue_fine)

""" Test checkout """
print(patron.check_out_book("1234567891234"))

""" Test overdue fine """
days_over = input("How many days overdue is the users book?: ")
print(patron.calculate_overdue_fine(int(days_over)))

""" Show final status """
print(patron)
