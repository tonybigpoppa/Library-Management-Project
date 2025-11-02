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
