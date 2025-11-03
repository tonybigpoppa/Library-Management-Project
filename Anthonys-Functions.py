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

class LibraryPatron:
    