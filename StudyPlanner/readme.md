
# 📚 StudyPlanner – Student Assistance System

<p align="center">
  <strong>Plan Your Studies. Manage Your Time. Track Your Progress.</strong>
</p>

<p align="center">
  A simple and organized study management application built with Pure Python and SQLite.
</p>

---

## 🌟 About The Project

**StudyPlanner** is a Python-based student productivity application designed to help students organize their academic activities in one place.

It provides a simple terminal-based interface where students can manage personal tasks, organize class timetables, save study notes, and track their learning progress.

The project is developed using **Pure Python without Django or any other web framework**, with SQLite for persistent data storage.

### 🎯 Project Objectives

- Organize daily academic activities.
- Manage personal study tasks and deadlines.
- Maintain class schedules.
- Store important study notes.
- Monitor study hours and learning progress.
- Provide a simple and structured student management system.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 User Authentication | Register and Login functionality |
| 📝 Personal Tasks | Add, view and complete study tasks |
| 📅 Class Timetable | Create and view class schedules |
| 📖 Study Notes | Save and view personal study notes |
| 📊 Study Progress | Record study hours and topics covered |
| 💾 Database Storage | Store information using SQLite |
| 👤 User-based Records | Keep records associated with individual users |

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| SQLite3 | Database management |
| SQL | Database queries and operations |
| hashlib | Password hashing |
| os | File and directory management |
| VS Codium | Development environment |
| Git & GitHub | Version control and collaboration |

**Architecture:** Modular Python Application

**Application Type:** Command-Line Interface (CLI)

**Framework:** No external web framework (Pure Python)

---

## 📁 Project Structure

```text
StudyPlanner/
│
├── main.py                     # Main application entry point
│
├── db.py                       # Database connection and table creation
│
├── auth.py                     # User registration and login
│
├── models/                     # Data models
│   ├── __init__.py
│   ├── task.py                 # Personal task model
│   ├── timetable.py            # Timetable model
│   ├── notes.py                # Study notes model
│   └── progress.py             # Study progress model
│
├── services/                   # Application business logic
│   ├── __init__.py
│   ├── task_service.py         # Task management operations
│   ├── timetable_service.py    # Timetable operations
│   ├── notes_service.py        # Notes management operations
│   └── progress_service.py     # Progress tracking operations
│
└── database/
    └── studyplanner.db         # SQLite database (generated locally)
```

### 📂 Directory Explanation

**1. `main.py` – Main Application**

Controls the application flow, displays menus, and connects different modules.

**2. `db.py` – Database Management**

Handles SQLite database connections and creates the required database tables.

**3. `auth.py` – Authentication**

Manages user registration, password hashing, and login verification.

**4. `models/` – Data Models**

Contains Python classes representing the main entities:

- `task.py` – PersonalTask
- `timetable.py` – Timetable
- `notes.py` – StudyNote
- `progress.py` – StudyProgress

**5. `services/` – Business Logic**

Contains the functions responsible for performing operations related to each application feature.

**6. `database/` – Data Storage**

Stores application records in the local SQLite database file.

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have installed:

- Python 3.8 or later
- VS Codium or any Python-supported editor
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/rimontanber96/Student-Assistance.git
```

### Step 2: Navigate to StudyPlanner

```bash
cd Student-Assistance/StudyPlanner
```

### Step 3: Run the Application

```bash
python main.py
```

**Note:** SQLite3 is included with standard Python installations in most environments. No external database server is required.

The database tables are created automatically when the application starts.

---

## 🚀 Application Workflow

```text
             START
               |
               v
        StudyPlanner App
               |
               v
          Main Menu
               |
       +-------+-------+
       |       |       |
       v       v       v
    Register  Login   Exit
                |
                v
          Authentication
                |
          Login Successful
                |
                v
         Student Dashboard
                |
      +---------+---------+
      |         |         |
      v         v         v
    Tasks   Timetable   Notes
      |
      v
   Progress
      |
      v
     Logout
      |
      v
    Main Menu
```

### Dashboard Modules

After successful login, users can access:

1. Personal Tasks
2. Class Timetable
3. Study Notes
4. Study Progress
5. Logout

---

## 🗄️ Database Design

The application uses SQLite as its local database.

### Database Tables

| Table | Purpose |
|---|---|
| `users` | Stores user credentials |
| `tasks` | Stores personal study tasks |
| `timetable` | Stores class schedules |
| `notes` | Stores study notes |
| `progress` | Stores study hours and topics |

### Database Relationships

Task, timetable, notes, and progress records contain a `user_id` field to associate records with their respective users.

---

## 🔒 Security

- Passwords are stored as hashes rather than plain text.
- PBKDF2-HMAC with SHA-256 is used for password hashing.
- Random salts are generated for password hashing.
- Parameterized SQL queries are used to reduce SQL injection risks.
- User-specific queries filter records using `user_id`.

**Security Note:** This is an educational project. Additional security improvements are needed before production deployment.

---

## 🧠 Python Concepts Used

This project demonstrates several fundamental Python concepts:

- Functions and Modules
- Classes and Objects
- Conditional Statements
- Loops (`while`, `for`)
- Exception Handling
- File and Directory Management
- Python Package Structure
- SQLite Database Connectivity
- SQL CRUD Operations
- Password Hashing

---

## 🔮 Future Improvements

The following features can be added in future versions:

- [ ] Edit and Delete Tasks
- [ ] Edit and Delete Study Notes
- [ ] Edit and Delete Timetable Entries
- [ ] Input Validation
- [ ] Study Progress Charts
- [ ] Daily and Weekly Study Reports
- [ ] Task Priority Filtering
- [ ] Deadline Reminders
- [ ] GUI-based Interface
- [ ] Automated Unit Testing

---

## 🎓 Learning Outcomes

Through this project, we aim to understand:

1. How to build a modular application using Pure Python.
2. How to connect Python with an SQLite database.
3. How to perform database operations using SQL.
4. How to implement basic user authentication.
5. How to organize code using modules, packages, and services.
6. How to manage application data using a structured approach.

---

## 👥 Project Information

**Project Name:** Student Assistance – StudyPlanner

**Project Category:** Student Productivity & Academic Management

**Programming Language:** Python

**Database:** SQLite

**Development Approach:** Modular Programming

**Repository:** [Student-Assistance](https://github.com/rimontanber96/Student-Assistance)

---

<p align="center">
  Made with ❤️ using Python
</p>

<p align="center">
  <strong>Study Smart. Stay Organized. Achieve More! 📚</strong>
</p>
