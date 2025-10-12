# Anthonys Functions
library = []

# Compute overdue fine
def overdue_fine(days_over, fine = 0.25, max_days = 14):
    """ 
    Calculates the fine for having a book overdue.
    
    fine = the daily fine for having an overdue book
    days_over = the amount of days overdue
    max_days = the max amount of days the fine will be calculated for

    """
    if days_over < max_days:
        return f"This users fine is: {days_over * fine}"
    else:
        return f"This user has hit the maximum fine of {max_days * fine}"
    

# Add book to library

# Declare book missing