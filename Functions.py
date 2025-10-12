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