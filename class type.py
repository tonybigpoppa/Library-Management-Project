#1 Validate_ISBN
 """Validate an ISBN-10 or ISBN-13 number.

   Returns:
        bool: True if valid ISBN, False otherwise.

    Raises:
        TypeError: If isbn_string is not a string.

            if not isinstance(isbn_string, str):
        raise TypeError("ISBN must be a string.")

    isbn = isbn_string.replace("-", "").replace(" ", "")
    if len(isbn) == 10:
        # Validate ISBN-10
        try:
            total = sum((10 - i) * (10 if x.upper() == "X" else int(x)) for i, x in enumerate(isbn))
            return total % 11 == 0
        except ValueError:
            return False
    elif len(isbn) == 13:
        # Validate ISBN-13
        try:
            total = sum((1 if i % 2 == 0 else 3) * int(x) for i, x in enumerate(isbn[:-1]))
            check_digit = (10 - (total % 10)) % 10
            return check_digit == int(isbn[-1])
        except ValueError:
            return False
    else:
        return False


        #2 Format_Bibliographic_Record()

        def format_bibliographic_record(title: str, author: str, year: int, publisher: str = None) -> str:
    """Format a bibliographic record for catalog display or citation.
   Args:
        title (str): The book's title.
        author (str): The author’s full name.
        year (int): Year of publication.
        publisher (str, optional): The book’s publisher.

    Returns:
        str: A formatted bibliographic record.

          if not isinstance(title, str) or not isinstance(author, str) or not isinstance(year, int):
        raise TypeError("Title and author must be strings, and year must be an integer.")
    if not title.strip() or not author.strip():
        raise ValueError("Title and author cannot be empty.")

    # Reformat author name: "Robert C. Martin" → "Martin, R. C."
    parts = author.split()
    if len(parts) > 1:
        last_name = parts[-1]
        initials = " ".join([p[0] + "." for p in parts[:-1]])
        author_formatted = f"{last_name}, {initials}"
    else:
        author_formatted = author

    record = f"{author_formatted} ({year}). {title}."
    if publisher:
        record += f" {publisher}."
    return record


#3 Searcg Catalog ()

def search_catalog(catalog: list[dict], keyword: str) -> list[dict]:
    """Search the library catalog for books matching a keyword.

    Args:
        catalog (list[dict]): A list of book entries where each entry is a dictionary
            containing 'title', 'author', 'genre', and 'isbn' keys.
        keyword (str): Keyword to search for (case-insensitive).

    Returns:
        list[dict]: A list of matching book dictionaries.

    Raises:
        TypeError: If catalog is not a list or keyword is not a string.
 if not isinstance(catalog, list) or not all(isinstance(book, dict) for book in catalog):
        raise TypeError("Catalog must be a list of dictionaries.")
    if not isinstance(keyword, str):
        raise TypeError("Keyword must be a string.")

    keyword = keyword.lower().strip()
    if not keyword:
        return []

    matches = []
    for book in catalog:
        for value in book.values():
            if isinstance(value, str) and keyword in value.lower():
                matches.append(book)
                break  
    return matches






"""

    The LibraryItem class represents a physical or digital item
    that can be borrowed by members. 

from datetime import datetime, timedelta


# ---------------------------
# Simulated Project 1 Integration Function
# ---------------------------
def calculate_due_date(loan_period_days: int) -> datetime:
    """
    Simulates a Project 1 utility function that calculates
    the due date based on the loan period.
    """
    return datetime.now() + timedelta(days=loan_period_days)


# ---------------------------
# LibraryItem Class
# ---------------------------
class LibraryItem:
    """
    Represents an item in the library collection.

    Attributes:
        item_id (str): Unique identifier for the item.
        title (str): The title of the item.
        item_type (str): Type of item ('book', 'dvd', etc.).
        loan_period (int): The number of days the item can be borrowed.
        _is_available (bool): Whether the item is currently available.

    Example:
        >>> item = LibraryItem("B001", "The Great Gatsby", "book", 14)
        >>> print(item)
        The Great Gatsby (book) - Available
        >>> due = item.checkout("M101")
        >>> print(due.date())
        2025-11-16
    """

    VALID_TYPES = {"book", "dvd", "magazine", "audiobook"}

    def __init__(self, item_id: str, title: str, item_type: str, loan_period: int = 14):
        """Initialize a LibraryItem with validation."""
        if not item_id.strip():
            raise ValueError("Item ID cannot be empty.")
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if item_type.lower() not in self.VALID_TYPES:
            raise ValueError(f"Invalid item type. Must be one of: {self.VALID_TYPES}")
        if loan_period <= 0:
            raise ValueError("Loan period must be a positive number of days.")

        self._item_id = item_id.strip()
        self._title = title.strip()
        self._item_type = item_type.lower()
        self._loan_period = loan_period
        self._is_available = True
        self._borrower_id = None

    
    @property
    def item_id(self) -> str:
        """str: Read-only unique identifier."""
        return self._item_id

    @property
    def title(self) -> str:
        """str: The title of the library item."""
        return self._title

    @title.setter
    def title(self, new_title: str):
        if not new_title.strip():
            raise ValueError("Title cannot be empty.")
        self._title = new_title.strip()

    @property
    def item_type(self) -> str:
        """str: The type of library item."""
        return self._item_type

    @property
    def is_available(self) -> bool:
        """bool: Whether the item is currently available."""
        return self._is_available

    @property
    def borrower_id(self) -> str:
        """str: The ID of the member who borrowed the item (if any)."""
        return self._borrower_id

    
    def checkout(self, member_id: str) -> datetime:
        """
        Check out the item to a member.

        Args:
            member_id (str): The ID of the member borrowing the item.

        Returns:
            datetime: The due date for the borrowed item.

        Raises:
            RuntimeError: If the item is not available.
        """
        if not self._is_available:
            raise RuntimeError(f"Item '{self._title}' is already checked out.")

        self._is_available = False
        self._borrower_id = member_id
        return calculate_due_date(self._loan_period)

    def checkin(self):
        """Mark the item as returned and available again."""
        self._is_available = True
        self._borrower_id = None

    def extend_loan(self, extra_days: int) -> int:
        """
        Extend the loan period for the item.

        Args:
            extra_days (int): Number of days to extend.

        Returns:
            int: The updated loan period.
        """
        if extra_days <= 0:
            raise ValueError("Extension days must be positive.")
        self._loan_period += extra_days
        return self._loan_period

    def status(self) -> str:
        """Return a string describing the item's current availability."""
        return "Available" if self._is_available else f"Checked out by {self._borrower_id}"

    # ----------------------------
    # Representations
    # ----------------------------
    def __str__(self):
        status = "Available" if self._is_available else f"Checked out to {self._borrower_id}"
        return f"{self._title} ({self._item_type}) - {status}"

    def __repr__(self):
        return (f"LibraryItem(item_id={self._item_id!r}, title={self._title!r}, "
                f"item_type={self._item_type!r}, loan_period={self._loan_period!r}, "
                f"is_available={self._is_available!r})")

