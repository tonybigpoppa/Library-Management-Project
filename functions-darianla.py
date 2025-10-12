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