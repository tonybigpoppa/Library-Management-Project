#Prince Olubuuse-Omisore
books = [
    {"title": "The Pragmatic Programmer", "available": True, "user": None},
    {"title": "Clean Code", "available": True, "user": None},
    {"title": "Python Crash Course", "available": False, "user": "Anthony"},
    {"title": "Automate the Boring Stuff", "available": True, "user": None},
    {"title": "Introduction to Algorithms", "available": False, "user": "Sarah"}
]

users = [
    {"name": "Anthony", "borrowed_books": ["Python Crash Course"]},
    {"name": "Sarah", "borrowed_books": ["Introduction to Algorithms"]},
    {"name": "Prince", "borrowed_books": []},
    {"name": "Jamal", "borrowed_books": []} 
]



# Function 1 Assigning book to user 
def assign_book_to_user(book_title, user_name, books, users):
    """""
    Assigns a book to a user if it is available in the library.

    book_title = title of the book to be assigned
    user_name = name of the user borrowing the book
    books = list of dictionaries containing book information
    users = list of dictionaries containing user information
    """

    if not isinstance(book_title, str) or not isinstance(user_name, str):
        raise TypeError("Book title and user name must be strings.")

    # Search for the book
    book_found = None
    for book in books:
        if book["title"].lower() == book_title.lower():
            book_found = book
            break

    if not book_found:
        raise ValueError(f"Book '{book_title}' not found in library.")

    # Check availability
    if not book_found["available"]:
        print(f"Sorry, '{book_title}' is currently checked out by {book_found['user']}.")
        return False

    # Find user
    user_found = None
    for user in users:
        if user["name"].lower() == user_name.lower():
            user_found = user
            break

    if not user_found:
        raise ValueError(f"User '{user_name}' not found in system.")

    # Assigning book to user
    book_found["available"] = False
    book_found["user"] = user_found["name"]
    user_found["borrowed_books"].append(book_found["title"])

    print(f"Book '{book_found['title']}' assigned to user '{user_found['name']}' successfully.")
    return True


"""Testing"""
title_input = input("Enter the title of the book to assign: ")
user_input = input("Enter the user borrowing the book: ")
assign_book_to_user(title_input, user_input, books, users)





# Function 2 Check book availability
def check_book_availability(book_title, books):
    """
    Checks if a given book is available for borrowing.
    """

    if not isinstance(book_title, str):
        raise TypeError("Book title must be a string.")

    for book in books:
        if book["title"].lower() == book_title.lower():
            if book["available"]:
                print(f"'{book['title']}' is available for borrowing.")
                return True
            else:
                print(f"'{book['title']}' is currently checked out by {book['user']}.")
                return False

    raise ValueError(f"Book '{book_title}' not found in library.")


""" Testing"""
title_check = input("Enter a book title to check availability: ")
check_book_availability(title_check, books)






#Function 3 Checking book format 
def format_book_name(title):
    """
    Formats a book title consistently.
    - Removes extra spaces
    - Converts to Title Case
    - Handles edge cases (empty strings or non-string input)
    """

    if not isinstance(title, str):
        raise TypeError("Title must be a string.")

    clean_title = title.strip()
    if not clean_title:
        raise ValueError("Title cannot be empty.")

    # Replacing multiple spaces with a single space
    while "  " in clean_title:
        clean_title = clean_title.replace("  ", " ")

    formatted_title = clean_title.title()

    print(f"Formatted title: '{formatted_title}'")
    return formatted_title


""" Testing """
title_to_format = input("Enter a book title to format: ")
format_book_name(title_to_format)

