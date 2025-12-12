# Library Project (INST326 Project 4 - Capstone-style)

## Overview
Small library management system:
- Manage books, patrons, and loans
- Persist data as JSON
- Import books from CSV and export books to CSV
- Unit, integration, and system tests using `unittest`

## Structure
(see project root for files)

## Requirements met
- Data persistence (save/load JSON)
- CSV import/export
- Error handling with exceptions
- `pathlib` and context managers used for I/O
- Tests: unit, integration, system (unittest)
- Documentation and sample data

## Setup (Python 3.8+)
1. Clone repository or copy files into `library_project/`
2. (Optional) Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\\Scripts\\activate on Windows
   pip install -r requirements.txt  # none required for base
