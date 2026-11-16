
from students import add_student, view_students
from attendance import mark_attendance, view_attendance
from reports import attendance_report


def main():
    while True:
        print("\n===== ATTENDANCE MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Mark Attendance")
        print("4. View Attendance")
        print("5. Attendance Report")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()

        elif choice == '2':
            view_students()

        elif choice == '3':
            mark_attendance()

        elif choice == '4':
            view_attendance()

        elif choice == '5':
            attendance_report()

        elif choice == '6':
            print("Thank you for using Attendance Management System!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
