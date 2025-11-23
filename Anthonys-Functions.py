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
is_checked_out = [False, False, True, False, True]  # True = checked out

days_over = input("How many days overdue is the users book?: ")

# 1: Compute overdue fine
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

#-----------------------------------------------------------------#

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


# Your original function
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

# Test Case
patron = LibraryPatron("John Doe", "P123", overdue_fine)

""" Test checkout """
print(patron.check_out_book("1234567891234"))

""" Test overdue fine """
days_over = input("How many days overdue is the users book?: ")
print(patron.calculate_overdue_fine(int(days_over)))

""" Show final status """
print(patron)
