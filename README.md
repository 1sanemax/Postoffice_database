# Postal Service Management System

## Overview
The **Postal Service Management System** is a desktop application designed to manage postal transactions including Post, Speedpost, and Parcel services. Built with Python, it leverages Tkinter for the GUI and MySQL for database management. The system supports user registration, login, transaction processing, and administrative functions such as viewing all transactions and editing user data.

This project was developed as a mini-project and demonstrates the integration of a relational database with a user-friendly interface for managing postal services.

## Features
- **User Management:**
  - User signup and login with validation.
  - Edit user details (username, password, city, phone, address).
  - Admin privileges for viewing and managing all transactions.
- **Services:**
  - **Post:** Basic postal service with sender and receiver details.
  - **Speedpost:** Faster delivery option with weight and priority settings.
  - **Parcel:** Supports weight, dimensions, and additional options (fragile, speed delivery, VPP).
- **Database Integration:**
  - Stores user data, transaction details, and admin records in MySQL.
  - Imports pincode and region data from CSV files.
- **Admin Features:**
  - View all transactions in a tabular format.
  - Edit user data with add, update, and delete functionalities.
  - Export transaction data to CSV files (under development).
- **GUI:**
  - Built with Tkinter for an intuitive user experience.
  - Includes input validation and error handling.

## Prerequisites
- **Python 3.x**: Ensure Python is installed on your system.
- **MySQL**: A local MySQL server must be running.
- **Required Python Libraries:**
  - `mysql-connector-python`
  - `pillow` (for image handling in Tkinter)
  - `tkinter` (usually included with Python)

Install the required libraries using pip:
```bash
pip install mysql-connector-python pillow

Setup Instructions
Clone the Repository:
git clone https://github.com/1sanemax/Postoffice_database.git
cd postal-service-management

Configure MySQL:
Install MySQL if not already installed.
Create a database named post_database:
CREATE DATABASE post_database;
Update the database credentials in the code if necessary (default: host=localhost, user=root, password=admin).
Prepare CSV Files:
Place your pincode and region CSV files in the directory:
The CSV files should have columns: SNO, Region, Pincodes.

Run the Application:
Start the application by running the main login script (e.g., login.py):
python login.py

Default Admin Credentials:
Username: admin
Password: Admin@123

postal-service-management/
│
├── login.py              # Main login and signup script
├── Services_Module.py    # Service selection and admin/user interface
├── Procedure_Module.py   # Postal service processing (Post, Speedpost, Parcel)
├── Repository.py         # Database operations and utility functions
├── User_login_logo.png   # Logo image for the login screen
└── README.md             # This file

login.py: Handles user authentication and initial database setup.

Services_Module.py: Manages the main service selection window and admin features.

Procedure_Module.py: Contains logic for processing Post, Speedpost, and Parcel transactions.

Repository.py: Includes database interaction functions and input validation.
Usage

Login/Signup:
Launch the application and either log in with existing credentials or sign up as a new user.
Admin users can log in with the default credentials to access additional features.

User Interface:
Regular users can select from Post, Speedpost, or Parcel services.
Enter sender and receiver details, including area and pincode selection from the database.

Admin Interface:
View all transactions in a table.
Edit user data (add, update, delete).
Export transaction data to CSV (feature in progress).
Transaction Processing:
Calculate costs based on weight, dimensions, and additional services (Parcel).
Save transactions to the database with timestamps.

Limitations
Currently supports only Tamil Nadu regions (pincode data).
CSV export functionality is partially implemented.
Hardcoded file paths (e.g., for CSV imports) need adjustment for portability.
Basic error handling; could be enhanced for production use.
Future Enhancements
Add support for multiple regions beyond Tamil Nadu.
Implement full CSV export functionality for all data views.
Enhance security (e.g., password hashing, secure admin credentials).
Add transaction history for individual users.
Improve portability by removing hardcoded paths.
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows PEP 8 guidelines and includes appropriate comments.

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m "Add feature").
Push to the branch (git push origin feature-branch).
Open a pull request.
License
This project is licensed under the MIT License. See the  file for details.

Acknowledgments
Developed as a mini-project for a Data Science course.
Thanks to the Tkinter and MySQL communities for their excellent documentation.

Last Updated: March 30, 2025
