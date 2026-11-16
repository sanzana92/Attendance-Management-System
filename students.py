
from database import connect_database


def add_student():
    conn = connect_database()
    if conn is None:
        return

    cursor = conn.cursor()

    reg_no = input("Enter Register Number: ")
    name = input("Enter Student Name: ")
    department = input("Enter Department: ")
    year = int(input("Enter Year: "))
    section = input("Enter Section: ")

    try:
        query = """
        INSERT INTO students
        (reg_no, name, department, year, section)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(query, (reg_no, name, department, year, section))
        conn.commit()

        print("Student added successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def view_students():
    conn = connect_database()
    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n===== STUDENT DETAILS =====")

    for student in students:
        print(student)

    cursor.close()
    conn.close()
