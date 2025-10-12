# Library-Management-Project
Function repository for the library management project. 

Project Description: 
The Library Management System is a Python-based application designed to help libraries manage their collections, members, and lending activities efficiently. It provides tools for tracking items, managing patron accounts, and processing checkouts, returns, and overdue notices.

Name	Role	Responsibilities:
[Member 1]	Project Lead / Coordinator	Oversees the overall project, assigns tasks, manages timeline, and ensures all requirements are met.
[Member 2]	Lead Developer	Designs and implements the main Python classes and core logic (book, member, and lending functions).
[Member 3]	Data Manager	Manages datasets, validates input/output, and ensures data consistency across modules.
[Anthony Palma]	Tester / Quality Assurance	Creates and executes test cases, ensures code reliability, and handles debugging.
[Darian La]	Documentation & Git Manager	Maintains README, docstrings, and handles Git commits, version control, and pull requests.

Domain Focus
Library and Information Science — developing a digital management system to handle books, members, and lending operations.

Problem Statement
Libraries face challenges managing large collections, tracking checkouts, and enforcing due dates efficiently.
This project provides a program that:
- Stores detailed information about library materials
- Tracks members and borrowing history
- Calculates due dates and overdue items
- Supports librarians with reports and easy data access

Installation and set up instructions: 
1. Use vscode to write function
2. git clone https://github.com/yourusername/library-management-system.git
3. push functions and all work to github through github desktop

Usage example for Key functions:
1. calculating due date
   from library_functions import calculate_due_date
   print(calculate_due_date("2025-10-12", 14))
2. add book
    important for when the library buys new books.
    uses and appends several lists responsible for keeping the library.

Function library overview and organization:

calculate_due_date(checkout_date, loan_period_days=14)	Calculates the due date for borrowed items.
due_status(days_out, max_days=14)	Determines whether an item is overdue or on time.
get_patron_info(patron_id, name, age, gender)	Returns a patron’s ID, name, age, and gender.
remove_book(titles, authors, is_checked_out, index)	Removes a book from records and keeps lists aligned.
[insert functions here]

Contribution Guidelines for all Team Members:
1. Add descriptive comments and docstrings to your code.
2. Test all new functions before committing.
3. Write clear, informative commit messages.
4. Add inline comments to clarify logic, especially for loops or conditionals.
5. Keep your code neat and consistent — use standard indentation (4 spaces) and follow Python best practices (PEP 8)
