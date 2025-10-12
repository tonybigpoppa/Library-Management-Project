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
        return f"This users fine is: {days_over * fine}"
    else:
        return f"This user has hit the maximum fine of {max_days * fine}"
    
    """Test case"""
overdue_fine(days_over)

#-----------------------------------------------------------------#

# 2: Add book to library
def add_book(titles, authors, isbn, is_checked_out, new_title, new_author, new_isbn):
    """
    Adds a new book to the library list of books.

    titles, authors, isbn, is_checked_out = these are all the lists that make up the current library of books
    new_title, new_author, new_isbn = the attributes of the new book being added

    """

    titles.append(new_title)
    authors.append(new_author)
    is_checked_out.append(False)
    return len(titles)

# 3: Declare book missing