from datetime import datetime, timedelta

# Reserve a book
def reserve_book(user_id: str, book_id: str, reservations: dict, reservation_days: int = 7) -> dict:
    """Reserve a book for a specific user."""
    if not isinstance(user_id, str) or not isinstance(book_id, str):
        raise TypeError("User ID and Book ID must be strings.")

    if book_id in reservations:
        raise ValueError(f"Book '{book_id}' is already reserved by another user.")

    due_date = (datetime.now() + timedelta(days=reservation_days)).strftime("%Y-%m-%d")
    reservations[book_id] = {"user_id": user_id, "due_date": due_date}
    return reservations


# Generate a simple QR text
def generate_book_qr(book_id: str, title: str, author: str) -> str:
    """Simulate generating a QR code for a book.

    This function doesn't create an actual image — instead, it returns a 
    text-based 'QR code' representation that can be displayed or saved.
    """
    if not all(isinstance(x, str) for x in [book_id, title, author]):
        raise TypeError("Book ID, title, and author must all be strings.")

    if not book_id or not title or not author:
        raise ValueError("Book ID, title, and author cannot be empty.")

    # QR text: a block of text showing book details
    qr_text = (
        f"========== BOOK QR ==========\n"
        f"Book ID : {book_id}\n"
        f"Title   : {title}\n"
        f"Author  : {author}\n"
        f"============================="
    )
    return qr_text


# Check reservation status
def check_reservation_status(book_id: str, reservations: dict) -> str:
    """Check if a book is reserved or available."""
    if not isinstance(book_id, str):
        raise TypeError("Book ID must be a string.")

    if not isinstance(reservations, dict):
        raise KeyError("Reservations data must be a dictionary.")

    if book_id not in reservations:
        return f"Book '{book_id}' is available for reservation."

    info = reservations[book_id]
    return f"Book '{book_id}' is reserved by user '{info['user_id']}' until {info['due_date']}."
