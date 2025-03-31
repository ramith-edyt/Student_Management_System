# Student-Management-System-Using-PyQt6
This project is a desktop application built using the PyQt6 framework and SQLite. It provides a user-friendly interface to manage student records, including adding, editing, deleting, and searching student details. The application is suitable for educational institutions and small-scale organizations to efficiently manage student data.
Key Features
1. Interactive GUI

    Built with PyQt6, offering a modern and responsive interface.
    Menu-driven navigation with file, help, and edit options.
    Dynamic toolbars and status bar interactions.

2. Core Functionalities

    Add Students: Add new student records to the database, including name, course, and mobile number.
    Edit Records: Modify existing student information directly from the table.
    Delete Records: Permanently delete student entries after confirmation.
    Search Students: Quickly find students by name.

3. Database Integration

    Uses SQLite for robust and lightweight database management.
    Automatically fetches and displays student data in a table view.

4. Data Interaction

    Table widget to display all student records.
    Clickable rows to enable record editing or deletion.
    Support for real-time updates to the table after database operations.

5. Dialogs for Better UX

    Pop-up dialogs for inserting, editing, and searching student details.
    Confirmation dialog for delete operations with success notifications.

6. Help and About Section

    Includes an "About" dialog to provide application details and usage information.

Screenshots

  Main Window: A screenshot of the main interface with student records displayed.
  Add/Edit Dialog: Screenshots of the forms used for adding or editing records.
  Search Functionality: A snapshot of the search dialog in action.

Getting Started
Prerequisites

    Python 3.8 or higher.
    Required Python libraries:
        PyQt6
        sqlite3

Install dependencies using:

    pip install PyQt6

Database Setup

The application uses a local SQLite database. A sample database.db file is included in the repository, which contains a table named students with the following structure:

    CREATE TABLE students (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      course TEXT NOT NULL,
      mobile TEXT NOT NULL
    );

Running the Application

    Clone the repository:

    git clone https://github.com/your_username/student-management-system.git
    cd student-management-system

Run the application:

    python main.py

File Structure

    main.py: The main application script containing the PyQt6 GUI and core functionalities.
    database.db: SQLite database file to store student records.
    icons/: Directory containing icons used in the application.
    README.md: Detailed project documentation.
