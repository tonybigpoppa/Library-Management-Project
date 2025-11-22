
1. Inheritance Hierarchy & Rationale

The system models different types of library items using an inheritance hierarchy:

AbstractItem (abstract base class)
Defines the shared interface (calculate_loan_period(), get_description()) for all library items. This ensures every subclass provides its own loan-period logic.

Book, DVD, Magazine (derived classes)
These classes inherit common behavior from AbstractItem while overriding loan-period rules.

Book → longest loan period

DVD → short loan period

Magazine → medium loan period

Rationale:
Inheritance reduces duplication since all items share attributes (title, genre) and behaviors but need specialized rules. Using an abstract base class enforces consistent structure.

2. Polymorphism

All item types implement their own version of calculate_loan_period().
When iterating over a list of AbstractItem objects, the system calls the correct subclass method automatically:

for item in items:
    print(item.calculate_loan_period())


Why it works:
Python resolves the method using dynamic dispatch, meaning the behavior depends on the actual object type—not the reference type.

3. Composition

The Library class has library items:

class Library:
    def __init__(self):
        self.items = []


The Library is not a type of item, so inheritance would be inappropriate. It simply contains items, making composition the natural choice.

4. Design Pattern Usage

Template Method Pattern (lightweight use)
AbstractItem defines the structure through an abstract method that subclasses must fill in.

Polymorphic Collection Pattern
Library stores a heterogeneous list of AbstractItem objects and processes them uniformly.

Short README Additions
Class Hierarchy Diagram
AbstractItem (ABC)
│
├── Book
├── DVD
└── Magazine

Polymorphism Example
items = [Book("Dune"), DVD("Inception"), Magazine("Time")]
for item in items:
    print(item.calculate_loan_period())


Same call → different outputs.

How Inheritance Helps

Removes repeated code (titles, categories)

Ensures consistent interface for all item types

Allows uniform processing through polymorphism