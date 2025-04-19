# Student Management System

## Introduction

This is a Student Management System created by Ahmed Abel Ojimah. It allows for managing students, generating QR codes, and creating student ID cards. The system is built using Python, Streamlit, and MySQL.

## Prerequisites

Ensure you have the following installed on your system:
1. **Python 3.8 or later**
2. **MySQL**
3. **Streamlit**
4. **Required Python libraries** (listed in the `requirements.txt` file)

## Setup Instructions

### Download and Install Python

- **Windows:**
  1. Download the Python installer from [python.org](https://www.python.org/downloads/windows/).
  2. Run the installer and ensure you check the box to "Add Python to PATH".
  3. Complete the installation.

- **macOS:**
  1. Download the Python installer from [python.org](https://www.python.org/downloads/macos/).
  2. Open the downloaded package and follow the installation instructions.

### Install MySQL

- **Windows:**
  1. Download the MySQL installer from [mysql.com](https://dev.mysql.com/downloads/installer/).
  2. Run the installer and follow the steps to install MySQL Server and MySQL Workbench.
  3. During installation, set a root password and remember it for later use.

- **macOS:**
  1. Download the MySQL DMG archive from [mysql.com](https://dev.mysql.com/downloads/mysql/).
  2. Open the DMG file and run the installer.
  3. Set a root password during installation.

### Setup MySQL Database

1. **Open MySQL Workbench (or use the command line):**
   - Create a new database named `student_management`.
   - Create the required tables using the following SQL commands:
     ```sql
     CREATE TABLE admins (
         id INT AUTO_INCREMENT PRIMARY KEY,
         username VARCHAR(255) NOT NULL,
         password VARCHAR(255) NOT NULL
     );

     CREATE TABLE students (
         id INT AUTO_INCREMENT PRIMARY KEY,
         name VARCHAR(255) NOT NULL,
         email VARCHAR(255) NOT NULL,
         phone VARCHAR(20) NOT NULL,
         address TEXT NOT NULL,
         department VARCHAR(100) NOT NULL,
         reg_no VARCHAR(100) NOT NULL,
         image LONGBLOB NOT NULL,
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

### Install Required Python Libraries

1. **Create and activate a virtual environment:**
   - **Windows:**
     ```sh
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS:**
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

2. **Install required libraries:**
   - Create a `requirements.txt` file with the following content:
     ```
     streamlit
     mysql-connector-python
     qrcode[pil]
     pillow
     pandas
     matplotlib
     ```

   - Install the libraries:
     ```sh
     pip install -r requirements.txt
     ```

### Download and Setup the Application

1. **Clone or download the source code from the repository:**
   - If you have a repository, use:
     ```sh
     git clone <repository_url>
     cd <repository_directory>
     ```
   - Alternatively, download the source code as a ZIP file and extract it to a desired directory.

2. **Navigate to the project directory in your terminal or command prompt:**
   ```sh
   cd <project_directory>
