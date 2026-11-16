# Attendance-Management-System

A desktop-based Attendance Management System developed using **Python, Tkinter, and MySQL**. The application provides a graphical interface to manage student details, record daily attendance, view attendance records, and generate attendance reports.

## Features

- **Add Student:** Add student details such as register number, name, department, year, and section.
- **View Students:** Display the list of registered students.
- **Mark Attendance:** Record a student's attendance as Present or Absent.
- **View Attendance:** View recorded attendance details.
- **Attendance Report:** Calculate the total classes, present days, absent days, and attendance percentage for each student.

## Technologies Used

- Python
- Tkinter (Graphical User Interface)
- MySQL (Database)
- MySQL Connector for Python
- Visual Studio Code

## Project Structure

```text
AttendanceManagementSystem/
├── gui.py
├── database.py
├── main.py
├── students.py
├── attendance.py
├── reports.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3
- MySQL Server
- Visual Studio Code (or another Python IDE)

## Installation and Setup

1. Clone this repository:

   ```bash
   git clone YOUR_REPOSITORY_URL
   ```

2. Open the project folder:

   ```bash
   cd AttendanceManagementSystem
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start your MySQL server.

5. Create a MySQL database named `attendance_management`.

6. Configure your MySQL connection details in `database.py`. Do not publish your actual database password.

7. Run the graphical application:

   ```bash
   python3 gui.py
   ```

## Database Tables

The application uses two main tables:

**Students**
- student_id
- reg_no
- name
- department
- year
- section

**Attendance**
- attendance_id
- student_id
- attendance_date
- status

## How to Use

1. Launch the application.
2. Select **Add Student** to register a student.
3. Select **Mark Attendance** to record attendance.
4. Use **View Students** to see registered students.
5. Use **View Attendance** to see attendance records.
6. Select **Attendance Report** to view attendance percentages.

## Future Improvements

- Search and filter student records.
- Update and delete student details.
- Export attendance reports to Excel or PDF.
- Add login authentication for administrators.

## Author

Developed as a student project using Python and MySQL.
