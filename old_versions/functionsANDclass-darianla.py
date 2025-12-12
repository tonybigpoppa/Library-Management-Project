#1.due date 
def due_status(days_out, max_days=14):
    """
    Determines whether a library item is on time or overdue.

    Parameters:
        days_out (int): The number of days the item has been checked out.
        max_days (int): The maximum allowed borrowing period (default is 14 days).

    Returns:
        str: A message indicating if the item is "On time" or how many days it is overdue.
    """
    if days_out <= max_days:
        return "On time"
    else:
        overdue_days = days_out - max_days
        return f"Overdue by {overdue_days} day(s)"

#2. remove book
def remove_book(titles, authors, is_checked_out, index):
    """
    Removes a book from the library's records based on its index.

    Parameters:
        titles (list): A list containing the titles of all books.
        authors (list): A list containing the authors corresponding to each title.
        is_checked_out (list): A list of booleans indicating whether each book is checked out.
        index (int): The position of the book to remove.

    Returns:
        tuple: A tuple containing the removed book's title and author.
    """
    removed_title = titles.pop(index)
    removed_author = authors.pop(index)
    is_checked_out.pop(index)
    return (removed_title, removed_author)
#3. patron information
def get_patron_info(patron_id: int, name: str, age: int, gender: str) -> dict:
    """
    Returns a library patron's information.
    
    Parameters:
        patron_id (int): Unique ID of the patron.
        name (str): Full name of the patron.
        age (int): Age of the patron.
        gender (str): Gender of the patron.
        
    Returns:
        dict: A dictionary containing patron information.
    """
    patron_info = {
        "Patron ID": patron_id,
        "Name": name,
        "Age": age,
        "Gender": gender
    }
    return patron_info
#CLASS FOR LIBRARY MANAGEMENT:
#This class is related to the due date function (#1) and get patron info function (#3)
class Reminder:
    """
    A class to manage and generate polite reminder messages for overdue library books.

    Attributes:
        _member_name (str): The member’s name.
        _title (str): The book title.
        _overdue_days (int): Number of days the book is overdue.

    Example:
        >>> reminder = Reminder("Alice", "1984", 5)
        >>> print(reminder.generate_message())
        Dear Alice, your book '1984' is 5 days overdue. Kindly return it soon.
    """

    def __init__(self, member_name, title, overdue_days):
        """
        Initialize a Reminder instance with validation.

        Args:
            member_name (str): Name of the library member.
            title (str): Title of the overdue book.
            overdue_days (int): Number of overdue days (0 if due today).

        Raises:
            ValueError: If any argument is invalid.
        """
        if not isinstance(member_name, str) or not member_name.strip():
            raise ValueError("member_name must be a non-empty string.")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string.")
        if not isinstance(overdue_days, int) or overdue_days < 0:
            raise ValueError("overdue_days must be a non-negative integer.")

        self._member_name = member_name.strip()
        self._title = title.strip()
        self._overdue_days = overdue_days

    # --- Properties with encapsulation ---
    @property
    def member_name(self):
        """Get or set the member's name."""
        return self._member_name

    @member_name.setter
    def member_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("member_name must be a non-empty string.")
        self._member_name = value.strip()

    @property
    def title(self):
        """Get or set the book title."""
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title must be a non-empty string.")
        self._title = value.strip()

    @property
    def overdue_days(self):
        """Get or set the number of overdue days."""
        return self._overdue_days

    @overdue_days.setter
    def overdue_days(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("overdue_days must be a non-negative integer.")
        self._overdue_days = value

    # --- Instance methods ---
    def generate_message(self):
        """Return a polite reminder message based on how overdue the book is."""
        days = self._overdue_days
        day_word = "day" if days == 1 else "days"

        if days == 0:
            return (f"Hello {self._member_name}, your book '{self._title}' is due today. "
                    f"Please return it on time. Thank you!")
        elif days <= 7:
            return (f"Dear {self._member_name}, your book '{self._title}' is {days} {day_word} overdue. "
                    "Kindly return it soon.")
        elif days <= 30:
            return (f"Dear {self._member_name}, your book '{self._title}' is {days} {day_word} overdue. "
                    "Please return it to avoid late fees.")
        else:
            return (f"Dear {self._member_name}, your book '{self._title}' is {days} {day_word} overdue. "
                    "Immediate return is required. Please contact the library if you need assistance.")

    def is_urgent(self):
        """Return True if the book is over 30 days overdue."""
        return self._overdue_days > 30

    def extend_due_date(self, extra_days):
        """
        Reduce overdue days to simulate granting an extension.

        Args:
            extra_days (int): Number of days to extend the due date.
        """
        if not isinstance(extra_days, int) or extra_days <= 0:
            raise ValueError("extra_days must be a positive integer.")
        self._overdue_days = max(0, self._overdue_days - extra_days)

    # --- String representations ---
    def __str__(self):
        """Return a user-friendly string representation."""
        return f"Reminder for {self._member_name}: '{self._title}' ({self._overdue_days} day(s) overdue)"

    def __repr__(self):
        """Return a detailed string representation for debugging."""
        return f"Reminder(member_name='{self._member_name}', title='{self._title}', overdue_days={self._overdue_days})"
