
from database import connect_database


def mark_attendance():
    conn = connect_database()
    if conn is None:
        return

    cursor = conn.cursor()

    student_id = int(input("Enter Student ID: "))
    attendance_date = input("Enter Date (YYYY-MM-DD): ")
    status = input("Enter Status (Present/Absent): ").capitalize()

    if status not in ["Present", "Absent"]:
        print("Invalid status!")
        cursor.close()
        conn.close()
        return

    try:
        query = """
        INSERT INTO attendance (student_id, attendance_date, status)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (student_id, attendance_date, status))
        conn.commit()

        print("Attendance marked successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()


def view_attendance():
    conn = connect_database()
    if conn is None:
        return

    cursor = conn.cursor()

    query = """
    SELECT a.attendance_id, s.name, a.attendance_date, a.status
    FROM attendance a
    JOIN students s ON a.student_id = s.student_id
    ORDER BY a.attendance_date DESC
    """

    cursor.execute(query)
    records = cursor.fetchall()

    print("\n===== ATTENDANCE DETAILS =====")

    for record in records:
        print(record)

    cursor.close()
    conn.close()
